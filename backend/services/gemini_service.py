import google.generativeai as genai
import json
import re
import os
from typing import List, Dict, Any
import asyncio
from dotenv import load_dotenv
from backend.models.place import Place

class GeminiService:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def search_places(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Search for places using Gemini AI with two-step validation
        """
        try:
            # Step 1: Get initial results
            prompt = self._create_search_prompt(city, area, place_type)
            print(f"🔍 Searching for {place_type} in {area}, {city}...")
            
            response = await self._generate_response(prompt)
            
            initial_places = self._parse_response(response)
            
            print(f"📋 Found {len(initial_places)} initial results, validating...")
            
            # Step 2: Validate each place exists
            validated_places = await self._validate_places(initial_places, city, area, place_type)
            
            print(f"🎯 Final result: {len(validated_places)} verified places")
            for i, place in enumerate(validated_places):
                print(f"   {i+1}. {place.get('name')} - {place.get('phone', 'No phone')}")
            
            return validated_places
        except Exception as e:
            print(f"❌ ERROR in Gemini search: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _create_search_prompt(self, city: str, area: str, place_type: str) -> str:
        """
        Create a structured prompt for Gemini AI with strict accuracy requirements
        """
        # Handle PG-specific searches
        if 'pg' in place_type.lower() or 'paying_guest' in place_type.lower():
            search_term = "paying guest accommodations" if 'mens' in place_type.lower() else "women's paying guest accommodations" if 'womens' in place_type.lower() else "paying guest accommodations"
            place_description = "PG accommodation"
        else:
            search_term = place_type
            place_description = place_type
            
        prompt = f"""Find popular and well-known {search_term} in {area}, {city}, India.

Provide 4-6 real places with complete details:

[
  {{
    "name": "Actual business name (e.g., Gold's Gym, Anytime Fitness, Cult.fit)",
    "address": "Complete street address, {area}, {city}, India",
    "phone": "+91-XXXXXXXXXX",
    "description": "Brief description of facilities/services"
  }}
]

REQUIREMENTS:
- Use real, popular business names that exist in {area}, {city}
- Include actual phone numbers in +91 format
- Provide complete street addresses
- Focus on well-known chains and established local businesses
- Return JSON only, no additional text

Location: {area}, {city}, India
Type: {search_term}"""
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
            return response.text
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
        Validate place data for quality and authenticity
        """
        name = place.get('name', '').strip()
        address = place.get('address', '').strip()
        
        # Basic validation
        if not name or not address:
            return False
        
        # Filter out obviously fake or suspicious names
        suspicious_patterns = [
            'example', 'sample', 'test', 'demo', 'placeholder',
            'fake', 'dummy', 'xyz', 'abc', 'lorem ipsum'
        ]
        
        name_lower = name.lower()
        for pattern in suspicious_patterns:
            if pattern in name_lower:
                return False
        
        # Address should contain the expected city/area
        address_lower = address.lower()
        
        # Very basic name validation - should not be too generic
        if len(name) < 3 or name.isdigit():
            return False
            
        # Name should not have excessive special characters
        special_char_count = sum(1 for char in name if not char.isalnum() and char not in [' ', '-', '.', '&', "'"])
        if special_char_count > 3:
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