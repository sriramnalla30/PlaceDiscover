import google.generativeai as genai
import json
import re
import os
from typing import List, Dict, Any
import asyncio
from dotenv import load_dotenv
from models.place import Place
import requests
from urllib.parse import quote_plus
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

class GeminiService:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        # Configure model with parameters for area-specific accuracy
        self.model = genai.GenerativeModel(
            'gemini-2.5-pro',
            generation_config={
                'temperature': 0.2,  # Balanced for area understanding
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
    
    async def search_places(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        PARALLEL SEARCH: Gemini 2.5-Pro + OpenStreetMap simultaneously
        Then merge, deduplicate, and enrich with phone numbers
        """
        try:
            print(f"\n{'='*80}")
            print(f"🚀 PARALLEL SEARCH INITIATED")
            print(f"📍 Location: {area}, {city}")
            print(f"🔍 Type: {place_type}")
            print(f"{'='*80}\n")
            
            # Execute both searches in PARALLEL
            print("⚡ Starting parallel execution...")
            gemini_task = asyncio.create_task(self._search_with_gemini(city, area, place_type))
            osm_task = asyncio.create_task(self._search_with_osm(city, area, place_type))
            
            # Wait for both to complete
            gemini_results, osm_results = await asyncio.gather(gemini_task, osm_task, return_exceptions=True)
            
            # Handle exceptions
            if isinstance(gemini_results, Exception):
                print(f"⚠️ Gemini search error: {gemini_results}")
                gemini_results = []
            if isinstance(osm_results, Exception):
                print(f"⚠️ OSM search error: {osm_results}")
                osm_results = []
            
            print(f"\n📊 RAW RESULTS:")
            print(f"   Gemini: {len(gemini_results)} places")
            print(f"   OSM: {len(osm_results)} places")
            
            # STEP 1: Filter both by area
            print(f"\n🔍 FILTERING BY AREA...")
            gemini_filtered = self._filter_by_area(gemini_results, area)
            osm_filtered = self._filter_by_area(osm_results, area)
            
            print(f"   After area filter:")
            print(f"   Gemini: {len(gemini_filtered)} places")
            print(f"   OSM: {len(osm_filtered)} places")
            
            # STEP 2: Merge and deduplicate
            print(f"\n🔄 MERGING AND DEDUPLICATING...")
            merged_results = self._merge_and_deduplicate(gemini_filtered, osm_filtered)
            print(f"   Merged: {len(merged_results)} unique places")
            
            # STEP 3: Enrich OSM results with phone numbers from Gemini
            print(f"\n📞 ENRICHING WITH PHONE NUMBERS...")
            enriched_results = await self._enrich_with_phone_numbers(merged_results, city, area)
            
            print(f"\n✅ FINAL RESULTS: {len(enriched_results)} places")
            print(f"{'='*80}\n")
            
            for i, place in enumerate(enriched_results[:6]):
                print(f"   {i+1}. {place.get('name')}")
                print(f"      📍 {place.get('address', '')[:60]}...")
                print(f"      📞 {place.get('phone', 'No phone')}")
                print(f"      🔖 Source: {place.get('source', 'Unknown')}")
                print()
            
            return enriched_results[:6]
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR in parallel search: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def _search_with_gemini(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Search using Gemini 2.5-Pro with explicit instruction to TAKE TIME
        """
        try:
            print(f"🤖 [GEMINI] Starting search...")
            
            prompt = self._create_realtime_prompt(city, area, place_type)
            
            # Add explicit instruction to take time
            prompt += """

⏱️ CRITICAL: TAKE YOUR TIME!
- Do NOT rush your response
- Carefully verify each business exists
- Double-check addresses contain the area name
- Think step-by-step before including any business
- Quality and accuracy are MORE important than speed
"""
            
            response = await self._generate_response(prompt)
            places = self._parse_response(response)
            
            # Mark source
            for place in places:
                place['source'] = 'Gemini 2.5-Pro'
            
            print(f"✅ [GEMINI] Retrieved {len(places)} places")
            return places
            
        except Exception as e:
            print(f"❌ [GEMINI] Error: {e}")
            return []
    
    async def _search_with_osm(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Search using OpenStreetMap/Nominatim (100% FREE)
        """
        try:
            print(f"🗺️  [OSM] Starting search...")
            
            # Run synchronous OSM calls in thread pool
            loop = asyncio.get_event_loop()
            places = await loop.run_in_executor(
                None,
                partial(self._osm_search_sync, city, area, place_type)
            )
            
            # Mark source
            for place in places:
                place['source'] = 'OpenStreetMap'
                place['phone'] = ''  # OSM doesn't provide phone
            
            print(f"✅ [OSM] Retrieved {len(places)} places")
            return places
            
        except Exception as e:
            print(f"❌ [OSM] Error: {e}")
            return []
    
    def _osm_search_sync(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Synchronous OpenStreetMap search
        """
        results = []
        
        try:
            # Map place types to OSM amenity tags
            amenity_map = {
                'gym': 'fitness_centre',
                'cafe': 'cafe',
                'restaurant': 'restaurant',
                'hospital': 'hospital',
                'hotel': 'hotel',
                'bank': 'bank',
                'atm': 'atm',
                'pharmacy': 'pharmacy'
            }
            
            amenity = amenity_map.get(place_type.lower(), place_type.lower())
            
            # Search query
            query = f"{amenity} in {area}, {city}, India"
            
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': query,
                'format': 'json',
                'limit': 10,
                'addressdetails': 1
            }
            headers = {
                'User-Agent': 'PlaceSearchApp/1.0 (place_search@example.com)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data:
                    # Extract name
                    name = item.get('display_name', '').split(',')[0]
                    if not name or len(name) < 3:
                        name = item.get('name', 'Unknown Place')
                    
                    # Build address
                    address_parts = []
                    address_data = item.get('address', {})
                    
                    if 'road' in address_data:
                        address_parts.append(address_data['road'])
                    if 'suburb' in address_data:
                        address_parts.append(address_data['suburb'])
                    if 'city' in address_data:
                        address_parts.append(address_data['city'])
                    if 'state' in address_data:
                        address_parts.append(address_data['state'])
                    if 'postcode' in address_data:
                        address_parts.append(address_data['postcode'])
                    
                    address = ', '.join(address_parts) if address_parts else item.get('display_name', '')
                    
                    results.append({
                        'name': name,
                        'address': address,
                        'phone': '',
                        'description': f"Found via OpenStreetMap. Type: {item.get('type', 'Unknown')}"
                    })
            
            # Respect OSM rate limit
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ OSM sync search error: {e}")
        
        return results
    
    def _filter_by_area(self, places: List[Dict[str, Any]], area: str) -> List[Dict[str, Any]]:
        """
        Filter places to only include those with area name in their address
        """
        filtered = []
        area_lower = area.lower().strip()
        
        # Handle common variations (e.g., "Benz Circle" vs "BenzCircle")
        area_variations = [
            area_lower,
            area_lower.replace(' ', ''),  # "benzcircle"
            area_lower.replace(' ', '-'),  # "benz-circle"
        ]
        
        for place in places:
            address = place.get('address', '').lower()
            
            # Check if any area variation is in the address
            if any(variation in address for variation in area_variations):
                filtered.append(place)
                print(f"   ✅ KEPT: {place.get('name')} (contains '{area}' in address)")
            else:
                print(f"   ❌ FILTERED OUT: {place.get('name')} (no '{area}' in address)")
        
        return filtered
    
    def _merge_and_deduplicate(self, gemini_results: List[Dict[str, Any]], osm_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge results from Gemini and OSM, remove duplicates
        Prefer Gemini data when duplicates found (has phone numbers)
        """
        merged = []
        seen_names = {}
        
        # Process Gemini results first (priority)
        for place in gemini_results:
            name_key = self._normalize_name(place.get('name', ''))
            if name_key not in seen_names:
                merged.append(place)
                seen_names[name_key] = place
                print(f"   ➕ Added from Gemini: {place.get('name')}")
            else:
                print(f"   🔄 Duplicate from Gemini (skipped): {place.get('name')}")
        
        # Process OSM results (check for duplicates)
        for place in osm_results:
            name_key = self._normalize_name(place.get('name', ''))
            
            if name_key not in seen_names:
                # Check if address is similar to existing places
                is_duplicate = False
                for existing_name, existing_place in seen_names.items():
                    if self._are_similar_places(place, existing_place):
                        is_duplicate = True
                        print(f"   🔄 Duplicate from OSM (similar to {existing_place.get('name')}): {place.get('name')}")
                        break
                
                if not is_duplicate:
                    merged.append(place)
                    seen_names[name_key] = place
                    print(f"   ➕ Added from OSM: {place.get('name')}")
            else:
                print(f"   🔄 Duplicate from OSM (exact match): {place.get('name')}")
        
        return merged
    
    def _normalize_name(self, name: str) -> str:
        """Normalize business name for comparison"""
        if not name:
            return ""
        
        # Remove common suffixes/prefixes and normalize
        name = name.lower()
        name = name.replace('the ', '')
        name = name.replace(' gym', '').replace(' cafe', '').replace(' restaurant', '')
        name = name.replace(' ', '').replace('-', '').replace('.', '')
        
        return name
    
    def _are_similar_places(self, place1: Dict[str, Any], place2: Dict[str, Any]) -> bool:
        """Check if two places are likely the same business"""
        
        # Compare names (fuzzy)
        name1 = self._normalize_name(place1.get('name', ''))
        name2 = self._normalize_name(place2.get('name', ''))
        
        if name1 == name2:
            return True
        
        # Check if one name is substring of other
        if len(name1) > 3 and len(name2) > 3:
            if name1 in name2 or name2 in name1:
                return True
        
        # Compare addresses (check for common parts)
        addr1 = place1.get('address', '').lower().split(',')
        addr2 = place2.get('address', '').lower().split(',')
        
        common_parts = set(addr1) & set(addr2)
        if len(common_parts) >= 2:  # At least 2 address parts match
            return True
        
        return False
    
    async def _enrich_with_phone_numbers(self, places: List[Dict[str, Any]], city: str, area: str) -> List[Dict[str, Any]]:
        """
        For places without phone numbers (from OSM), ask Gemini to find them
        This is done in BATCHES to be efficient
        """
        
        # Separate places with and without phones
        with_phone = [p for p in places if p.get('phone')]
        without_phone = [p for p in places if not p.get('phone')]
        
        if not without_phone:
            print(f"   All places already have phone numbers!")
            return places
        
        print(f"   Need to enrich {len(without_phone)} places with phone numbers...")
        
        # Batch enrichment (process multiple at once)
        enriched = []
        batch_size = 3
        
        for i in range(0, len(without_phone), batch_size):
            batch = without_phone[i:i+batch_size]
            
            try:
                # Create prompt for batch
                prompt = f"""Find REAL phone numbers for these businesses in {area}, {city}:

"""
                for j, place in enumerate(batch, 1):
                    prompt += f"{j}. {place.get('name')} at {place.get('address', '')}\n"
                
                prompt += """
INSTRUCTIONS:
- Search for the ACTUAL phone number of each business
- ONLY provide phone number if you're 95%+ confident it's correct
- If not found, return "Not available"
- Format: Just the phone number, no other text
- TAKE YOUR TIME to find accurate data

Respond in JSON:
[
  {"business": "Name", "phone": "number or Not available"},
  ...
]
"""
                
                # Use faster model for phone lookup (to reduce wait time)
                phone_model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash-exp",  # Faster for simple lookups
                    generation_config={
                        'temperature': 0.2,
                        'top_p': 0.9,
                        'top_k': 40,
                        'max_output_tokens': 512,
                    }
                )
                
                response = await asyncio.to_thread(
                    phone_model.generate_content, prompt
                )
                
                # Parse response - handle different formats
                try:
                    response_text = response.text.strip()
                except:
                    # Use parts accessor
                    if response.candidates and len(response.candidates) > 0:
                        candidate = response.candidates[0]
                        if candidate.content and candidate.content.parts:
                            response_text = ''.join(part.text for part in candidate.content.parts if hasattr(part, 'text')).strip()
                        else:
                            raise Exception("No valid response content")
                    else:
                        raise Exception("No candidates in response")
                
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                
                phone_data = json.loads(response_text)
                
                # Update places with phone numbers
                for place, data in zip(batch, phone_data):
                    phone = data.get('phone', 'Not available')
                    if phone and phone != 'Not available':
                        place['phone'] = phone
                        place['source'] = f"{place['source']} + Gemini Phone"
                        print(f"   📞 Enriched: {place.get('name')} -> {phone}")
                    else:
                        print(f"   ⚠️ No phone found: {place.get('name')}")
                
                enriched.extend(batch)
                
                # Delay between batches (respect rate limits)
                await asyncio.sleep(1.5)
                
            except Exception as e:
                print(f"   ⚠️ Phone enrichment error for batch: {e}")
                # Add places without enrichment
                enriched.extend(batch)
        
        # Combine all results
        final_results = with_phone + enriched
        
        return final_results
    
    def _create_realtime_prompt(self, city: str, area: str, place_type: str) -> str:
        """
        Create REAL-TIME focused prompt for latest, accurate business data
        """
        # Handle PG-specific searches
        if 'pg' in place_type.lower() or 'paying_guest' in place_type.lower():
            search_term = "paying guest accommodations" if 'mens' in place_type.lower() else "women's paying guest accommodations" if 'womens' in place_type.lower() else "paying guest accommodations"
        else:
            search_term = place_type
            
        prompt = f"""
🎯 ULTRA-STRICT AREA-SPECIFIC BUSINESS SEARCH
Location: ONLY businesses in {area} area of {city}, India
Business Type: {search_term}

⚠️ CRITICAL LOCATION REQUIREMENT - THIS IS MANDATORY:
🚨 ONLY include businesses that are physically located IN THE {area} AREA SPECIFICALLY
🚨 DO NOT include businesses from nearby areas like Labbipet, Patamata, or other localities
🚨 The address MUST explicitly mention "{area}" or be within {area} boundaries
🚨 When uncertain about exact area location, DO NOT INCLUDE the business

⚠️ CRITICAL REQUIREMENTS - READ CAREFULLY:

1. **EXACT AREA MATCH (HIGHEST PRIORITY)**:
   - Business MUST be physically located IN {area} area - this is NON-NEGOTIABLE
   - Address should explicitly mention "{area}" in it
   - DO NOT include businesses from adjacent/nearby areas even if they're close
   - If you're not 100% certain the business is in {area}, exclude it
   - Being in the same city is NOT enough - must be in the specific area

2. **LATEST & CURRENT DATA ONLY**:
   - Focus on businesses that are CURRENTLY operational (2024-2025)
   - Include both popular chains AND well-known local establishments
   - Prioritize businesses with recent activity/reviews
   - NO closed or permanently shut businesses
   - NO businesses from outdated information

3. **ACCURACY IS PARAMOUNT**:
   - Each business must be a REAL, verifiable establishment
   - NO generic names like "New Gym", "Best Cafe", "City Restaurant"
   - NO made-up combinations or placeholder names
   - NO fictional addresses

4. **DATA QUALITY STANDARDS**:
   ✅ Business Name: Must be the EXACT real name (check spelling carefully)
   ✅ Address: Must explicitly mention {area} and be in that area
   ✅ Phone Number: Only include if you're CERTAIN it's correct (format: +91-XXXXXXXXXX)
   ✅ If unsure about phone number, use null instead of guessing
   
5. **WHAT TO INCLUDE**:
   - Well-established local businesses IN {area} (if famous in the area)
   - National/international chains with presence IN {area} specifically
   - Popular establishments IN {area} with good reputation

6. **STRICT ANTI-HALLUCINATION RULES**:
   ❌ DO NOT create business names by combining random words
   ❌ DO NOT guess addresses
   ❌ DO NOT include a business if you're less than 95% certain it exists IN {area}
   ❌ DO NOT make up phone numbers
   ❌ DO NOT include businesses from other areas of {city}

7. **AREA VERIFICATION CHECKLIST** (Ask yourself for EACH business):
   □ Is this business physically IN THE {area} AREA (not just nearby)?
   □ Does the address explicitly mention {area}?
   □ Can I confirm this is within {area} boundaries?
   □ Am I 100% certain about the area location?
   □ If someone goes to {area}, will they find this business there?

8. **RESULT EXPECTATIONS**:
   - Return 3-6 businesses maximum (quality > quantity)
   - ALL businesses MUST be in {area} area specifically
   - If you can only find 1-2 businesses truly IN {area}, that's acceptable
   - Better to return 0 results than include businesses from wrong areas
   - DO NOT fill results with nearby area businesses

9. **OUTPUT FORMAT** (STRICT JSON ONLY - NO MARKDOWN):
[
  {{
    "name": "Exact Real Business Name",
    "address": "Complete address that MENTIONS {area}, {city}, State, Pincode",
    "phone": "+91-XXXXXXXXXX or null if uncertain",
    "description": "Brief 1-2 sentence description"
  }}
]

🚨 FINAL CRITICAL REMINDER: 
- ALL businesses MUST be in {area} area - NOT Labbipet, NOT Patamata, NOT other nearby areas
- Location accuracy is MORE important than returning many results
- If no businesses in {area} match criteria, return empty array []
- When in doubt about area location, LEAVE IT OUT

SEARCH AREA: {area} (and ONLY {area})
CITY: {city}
BUSINESS TYPE: {search_term}

Now provide results for {search_term} that are PHYSICALLY LOCATED IN {area} AREA of {city}, India.
Return ONLY the JSON array with NO additional text:
"""
        return prompt
    
    def _create_search_prompt(self, city: str, area: str, place_type: str) -> str:
        """
        Create high-accuracy search prompt with strict real business requirements
        """
        # Handle PG-specific searches
        if 'pg' in place_type.lower() or 'paying_guest' in place_type.lower():
            search_term = "paying guest accommodations" if 'mens' in place_type.lower() else "women's paying guest accommodations" if 'womens' in place_type.lower() else "paying guest accommodations"
            place_description = "PG accommodation"
        else:
            search_term = place_type
            place_description = place_type
            
        prompt = f"""
        HIGH-ACCURACY BUSINESS SEARCH for {search_term} in {area}, {city}, India
        
        🎯 ACCURACY MISSION: Find REAL businesses that actually exist and are operational.
        
        MANDATORY VERIFICATION PROCESS:
        1. ✅ REAL BUSINESS CHECK:
           - Must be an actual established business (not made-up names)
           - Should have been operating for at least 6 months
           - Must have real customers and reviews
        
        2. ✅ LOCATION VERIFICATION:
           - Business must actually exist in {area}, {city}
           - Address should be verifiable on Google Maps
           - No fictional addresses or combinations
        
        3. ✅ BUSINESS TYPES TO PRIORITIZE:
           - Well-known local establishments with good reputation
           - Popular franchises and chains
           - Businesses mentioned in local directories
           - Establishments with online presence
        
        4. ❌ NEVER INCLUDE:
           - Generic names like "Best Gym" or "New Restaurant"
           - Made-up business name combinations
           - Businesses you're not 100% certain exist
           - Placeholder or example names
        
        5. 📞 PHONE NUMBER ACCURACY:
           - Only include if you're certain it's correct
           - Must be in +91-XXXXXXXXXX format
           - Use null if uncertain
        
        JSON RESPONSE (4-5 businesses maximum):
        [
            {{
                "name": "Real verified business name",
                "address": "Actual street address, {area}, {city}, India",
                "phone": "+91-XXXXXXXXXX or null",
                "description": "Specific services/facilities offered"
            }}
        ]
        
        ⚠️ QUALITY OVER QUANTITY: Better to return 2 real businesses than 6 questionable ones.
        
        Location: {area}, {city}, India
        Type: {search_term}
        """
        return prompt
    
    async def _validate_places(self, places: List[Dict[str, Any]], city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Validate each place by asking Gemini if it actually exists
        """
        validated_places = []
        
        for i, place in enumerate(places):
            print(f"🔍 Validating: {place.get('name', 'Unknown')}")
            
            validation_prompt = f"""CRITICAL BUSINESS VERIFICATION TASK
You are a fact-checker verifying if this business ACTUALLY EXISTS in the real world.

BUSINESS DETAILS TO VERIFY:
- Name: {place.get('name', 'Unknown')}
- Address: {place.get('address', 'Unknown')}
- Phone: {place.get('phone', 'Unknown')}
- Type: {place_type}
- Location: {area}, {city}, India

MANDATORY VERIFICATION STEPS:
You must check ALL of these sources and be EXTREMELY STRICT:

1. **Google Maps Verification**: 
   - Is this exact business name listed on Google Maps at this address?
   - Does the address actually exist in {area}, {city}?
   - Are there recent reviews (within last 6 months)?

2. **Official Website/Company Verification**:
   - Does the company's official website list this specific location?
   - For chains (Gold's Gym, Cult.fit, F45, etc.), check their official store locator

3. **Phone Number Verification**:
   - Is this phone number actually associated with this specific business?
   - Does calling this number reach this business? (based on online listings)

4. **Multiple Directory Verification**:
   - Is it listed on Justdial, Sulekha, or other Indian business directories?
   - Are the details consistent across multiple sources?

5. **Local Knowledge Check**:
   - Does this business make sense for {area}, {city}?
   - Is the address format and area name correct for this city?

6. **Recent Activity Verification**:
   - Are there recent reviews, social media posts, or activity?
   - Is there evidence it's currently operational (not permanently closed)?

CRITICAL RULES:
- If you find ANY inconsistency or cannot verify through multiple sources, mark as "exists": false
- Only mark "exists": true if you can verify through AT LEAST 3 different reliable sources
- Be EXTREMELY CONSERVATIVE - it's better to reject 10 real businesses than include 1 fake one
- If the business name seems like a made-up combination, mark as false
- If you cannot find recent evidence of operation, mark as false

RETURN FORMAT (JSON only):
{{
  "exists": true/false,
  "confidence": "high/medium/low",
  "verification_sources": ["List of sources where you found this business"],
  "inconsistencies": ["List any inconsistencies found"],
  "reason": "Detailed explanation with evidence from multiple sources",
  "corrected_name": "Actual name if different",
  "corrected_address": "Actual address if different", 
  "corrected_phone": "Actual phone if different"
}}

REMEMBER: Your job is to REJECT questionable businesses. Only approve if you have SOLID EVIDENCE from multiple sources."""

            try:
                validation_response = await self._generate_response(validation_prompt)
                
                # Parse validation response
                validation_result = self._parse_validation_response(validation_response)
                
                # STRICT VALIDATION CRITERIA
                exists = validation_result.get('exists', False)
                confidence = validation_result.get('confidence', '').lower()
                sources = validation_result.get('verification_sources', [])
                inconsistencies = validation_result.get('inconsistencies', [])
                
                # Only accept if:
                # 1. exists = true
                # 2. confidence = high (no medium or low accepted)
                # 3. At least 2 verification sources
                # 4. No major inconsistencies
                if (exists and 
                    confidence == 'high' and 
                    len(sources) >= 2 and 
                    len(inconsistencies) == 0):
                    
                    # Place passed strict validation - use corrected values only if they exist and are not null
                    corrected_name = validation_result.get('corrected_name')
                    corrected_address = validation_result.get('corrected_address') 
                    corrected_phone = validation_result.get('corrected_phone')
                    
                    validated_place = {
                        'name': corrected_name if corrected_name and corrected_name.strip() else place.get('name', ''),
                        'address': corrected_address if corrected_address and corrected_address.strip() else place.get('address', ''),
                        'phone': corrected_phone if corrected_phone and corrected_phone.strip() else place.get('phone', ''),
                        'description': place.get('description', ''),
                        'validation_status': f"✅ VERIFIED ({len(sources)} sources, high confidence)",
                        'validation_reason': validation_result.get('reason', 'No reason provided'),
                        'verification_sources': sources
                    }
                    validated_places.append(validated_place)
                    print(f"✅ VERIFIED: {validated_place['name']} ({len(sources)} sources)")
                    
                else:
                    print(f"❌ REJECTED: {place.get('name')} - {validation_result.get('reason', 'Failed validation')[:50]}...")
                    
            except Exception as e:
                print(f"❌ Validation error for {place.get('name', 'Unknown')}: {e}")
                # If validation fails, exclude the place to be safe
                continue
        
        return validated_places
    
    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """
        Parse validation response from Gemini
        """
        try:
            # Clean the response
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = re.sub(r'^```json\s*', '', cleaned_response)
            if cleaned_response.endswith('```'):
                cleaned_response = re.sub(r'\s*```$', '', cleaned_response)
            
            validation_data = json.loads(cleaned_response)
            return validation_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Validation JSON parse error: {e}")
            return {'exists': False, 'confidence': 'low', 'reason': 'Failed to parse validation response'}
        except Exception as e:
            print(f"❌ Validation parse error: {e}")
            return {'exists': False, 'confidence': 'low', 'reason': 'Validation error'}
    
    async def _generate_response(self, prompt: str) -> str:
        """
        Generate response from Gemini AI
        """
        try:
            # Use asyncio to run the synchronous Gemini API call
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(prompt)
            )
            
            # Handle different response formats
            try:
                # Try simple text accessor
                return response.text
            except:
                # Fall back to parts accessor
                if hasattr(response, 'candidates') and response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                        texts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        if texts:
                            return ''.join(texts)
                
                raise Exception(f"No valid response content found")
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise
    
    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse Gemini response into structured place data
        """
        try:
            # Clean the response - remove markdown formatting if present
            cleaned_response = response.strip()
            
            if cleaned_response.startswith('```json'):
                cleaned_response = re.sub(r'^```json\s*', '', cleaned_response)
            if cleaned_response.endswith('```'):
                cleaned_response = re.sub(r'\s*```$', '', cleaned_response)
            
            # Parse JSON
            places_data = json.loads(cleaned_response)
            
            # Validate and clean data
            places = []
            for i, place_data in enumerate(places_data[:8]):  # Limit to 8 places
                if isinstance(place_data, dict) and 'name' in place_data:
                    place = {
                        'name': place_data.get('name', '').strip(),
                        'address': place_data.get('address', '').strip(),
                        'phone': self._clean_phone_number(place_data.get('phone', '')),
                        'description': place_data.get('description', '').strip()
                    }
                    
                    # Validate place data quality
                    if self._is_valid_place(place):
                        places.append(place)
            
            return places
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Raw response that failed: {response}")
            return self._create_fallback_response()
        except Exception as e:
            print(f"❌ Response parsing error: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_response()
    
    def _clean_phone_number(self, phone: str) -> str:
        """
        Clean and format phone number
        """
        if not phone:
            return ""
        
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Ensure Indian format
        if cleaned.startswith('+91'):
            return cleaned
        elif cleaned.startswith('91') and len(cleaned) >= 12:
            return '+' + cleaned
        elif len(cleaned) == 10:
            return '+91-' + cleaned
        
        return phone  # Return original if can't clean
    
    def _is_valid_place(self, place: Dict[str, Any]) -> bool:
        """
        Enhanced validation for business authenticity - allows both chains and local businesses
        """
        name = place.get('name', '').strip()
        address = place.get('address', '').strip()
        
        # Basic validation
        if not name or not address:
            return False
        
        # Suspicious pattern detection (only obvious fakes)
        suspicious_patterns = [
            'example', 'sample', 'test', 'demo', 'placeholder',
            'fake', 'dummy', 'xyz cafe', 'abc restaurant', 'lorem ipsum',
        ]
        
        name_lower = name.lower()
        for pattern in suspicious_patterns:
            if pattern in name_lower:
                return False
        
        # Reject ONLY obviously generic patterns (too vague)
        generic_patterns = [
            r'^(the |a |an )?(new|best|top|good|nice|great)\s+(gym|cafe|restaurant|hotel)$',
            r'^(city|local|area|main)\s+(gym|cafe|restaurant)$',
        ]
        
        for pattern in generic_patterns:
            if re.search(pattern, name_lower):
                return False
        
        # Name length validation
        if len(name) < 3 or len(name) > 80:
            return False
            
        # Reject pure numbers or excessive special characters
        if name.isdigit():
            return False
            
        special_char_count = sum(1 for char in name if not char.isalnum() and char not in [' ', '-', '.', '&', "'", '(', ')', ','])
        if special_char_count > 6:
            return False
        
        # Address validation (more lenient)
        if len(address) < 10 or 'example' in address.lower():
            return False
            
        return True
    
    def _create_fallback_response(self) -> List[Dict[str, Any]]:
        """
        Create fallback response when AI parsing fails
        """
        return [
            {
                "name": "Search results temporarily unavailable",
                "address": "Please try again in a moment",
                "phone": "",
                "description": "Service is processing your request"
            }
        ]
    


    async def _verify_with_web_search(self, ai_places: List[Dict], city: str, area: str, place_type: str) -> List[Dict]:
        """
        Verify AI suggestions using free web search (DuckDuckGo + JustDial)
        """
        verified_places = []
        
        for place in ai_places:
            try:
                business_name = place.get('name', '')
                search_query = f"{business_name} {area} {city}"
                
                print(f"   🔍 Web verifying: {business_name}")
                
                # Check multiple free sources
                verification_score = 0
                
                # 1. DuckDuckGo search
                if await self._check_duckduckgo(search_query):
                    verification_score += 2
                
                # 2. JustDial search  
                if await self._check_justdial(search_query, place_type):
                    verification_score += 2
                
                # 3. Google search (basic)
                if await self._check_google_basic(search_query):
                    verification_score += 1
                
                # Require at least 2 points to verify
                if verification_score >= 2:
                    print(f"   ✅ Verified: {business_name} (score: {verification_score})")
                    verified_places.append(place)
                else:
                    print(f"   ❌ Not verified: {business_name} (score: {verification_score})")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"   ⚠️ Verification error for {place.get('name')}: {e}")
        
        return verified_places

    async def _check_duckduckgo(self, search_query: str) -> bool:
        """
        Search DuckDuckGo for business existence
        """
        try:
            url = f"https://duckduckgo.com/html/?q={quote_plus(search_query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                content = response.text.lower()
                # Look for business indicators
                business_indicators = ['phone', 'address', 'reviews', 'hours', 'contact', 'website']
                return any(indicator in content for indicator in business_indicators)
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        
        return False

    async def _check_justdial(self, search_query: str, place_type: str) -> bool:
        """
        Search JustDial for business existence
        """
        try:
            # JustDial search URL
            url = f"https://www.justdial.com/functions/ajax_search.php"
            params = {
                'q': search_query,
                'city': 'All+India'
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                content = response.text.lower()
                # Check if business name appears in results
                query_words = search_query.lower().split()
                return len([word for word in query_words if word in content]) >= 2
                
        except Exception as e:
            print(f"JustDial search error: {e}")
        
        return False

    async def _check_google_basic(self, search_query: str) -> bool:
        """
        Basic Google search for business existence (limited due to rate limits)
        """
        try:
            url = f"https://www.google.com/search?q={quote_plus(search_query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                content = response.text.lower()
                # Simple existence check
                business_name = search_query.split()[0].lower()
                return business_name in content and ('address' in content or 'phone' in content)
                
        except Exception as e:
            print(f"Google search error: {e}")
        
        return False