"""
Hybrid Search Service - Combines SerpStack + Gemini for best results
SerpStack gives real Google data, Gemini enriches with additional details
"""
import asyncio
from typing import List, Dict, Any
from services.serpstack_service import SerpStackService
from services.gemini_service import GeminiService

class HybridSearchService:
    def __init__(self):
        self.serpstack = SerpStackService()
        self.gemini = GeminiService()
    
    async def search_places(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Hybrid search strategy:
        1. Get REAL results from SerpStack (Google SERP)
        2. If needed, enrich with Gemini for missing phone numbers
        3. Return combined, deduplicated results
        """
        try:
            print(f"\n{'='*80}")
            print(f"🚀 HYBRID SEARCH (SerpStack + Gemini)")
            print(f"📍 Location: {area}, {city}")
            print(f"🔍 Type: {place_type}")
            print(f"{'='*80}\n")
            
            # STEP 1: Get real Google data from SerpStack
            print("🔍 [STEP 1] Fetching real Google search results...")
            serpstack_results = self.serpstack.search_places(city, area, place_type)
            
            if not serpstack_results:
                print("⚠️ No SerpStack results, falling back to Gemini only...")
                return await self.gemini.search_places(city, area, place_type)
            
            print(f"✅ SerpStack returned {len(serpstack_results)} results")
            
            # STEP 2: Check if we need phone enrichment
            results_without_phone = [
                p for p in serpstack_results 
                if not p.get('phone') or len(p.get('phone', '').strip()) < 5
            ]
            
            if results_without_phone:
                print(f"\n📞 [STEP 2] Enriching {len(results_without_phone)} results with phone numbers...")
                enriched = await self._enrich_with_gemini_phones(
                    results_without_phone, 
                    city, 
                    area
                )
                
                # Update original results with enriched data
                for original in serpstack_results:
                    for enriched_place in enriched:
                        if self._are_same_place(original, enriched_place):
                            original['phone'] = enriched_place.get('phone', original['phone'])
                            original['source'] = f"{original['source']} + Gemini"
                            break
            
            # STEP 3: Validate results are in correct area
            print(f"\n🎯 [STEP 3] Filtering by area '{area}'...")
            filtered_results = self._filter_by_area(serpstack_results, area)
            
            print(f"\n✅ FINAL: {len(filtered_results)} places")
            print(f"{'='*80}\n")
            
            for i, place in enumerate(filtered_results, 1):
                print(f"{i}. {place.get('name')}")
                print(f"   📍 {place.get('address', '')[:60]}...")
                print(f"   📞 {place.get('phone', 'No phone')}")
                print(f"   🔖 {place.get('source', 'Unknown')}")
                if place.get('rating'):
                    print(f"   ⭐ {place['rating']} ({place.get('reviews', 0)} reviews)")
                print()
            
            return filtered_results
            
        except Exception as e:
            print(f"❌ Hybrid search error: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to Gemini only
            print("⚠️ Falling back to Gemini-only search...")
            return await self.gemini.search_places(city, area, place_type)
    
    async def _enrich_with_gemini_phones(
        self, 
        places: List[Dict[str, Any]], 
        city: str, 
        area: str
    ) -> List[Dict[str, Any]]:
        """
        Use Gemini to find phone numbers for places that don't have them
        """
        import google.generativeai as genai
        
        enriched = []
        batch_size = 3
        
        for i in range(0, len(places), batch_size):
            batch = places[i:i+batch_size]
            
            try:
                # Create prompt for batch
                prompt = f"""Find REAL phone numbers for these businesses in {area}, {city}, India:

"""
                for j, place in enumerate(batch, 1):
                    prompt += f"{j}. {place.get('name')} at {place.get('address', '')}\n"
                
                prompt += """
INSTRUCTIONS:
- Search for the ACTUAL, CURRENT phone number of each business
- ONLY provide phone number if you're 95%+ confident it's correct
- If not found, return "Not available"
- Use Indian format: +91-XXXXXXXXXX
- TAKE YOUR TIME to find accurate data

Respond in JSON:
[
  {"business": "Name", "phone": "+91-XXXXXXXXXX or Not available"},
  ...
]
"""
                
                # Use Gemini for phone lookup
                phone_model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash-exp",
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
                
                # Parse response
                import json
                response_text = response.text.strip()
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                
                phone_data = json.loads(response_text)
                
                # Update places with phone numbers
                for place, data in zip(batch, phone_data):
                    phone = data.get('phone', 'Not available')
                    if phone and phone != 'Not available':
                        place['phone'] = phone
                        print(f"   📞 Enriched: {place.get('name')} -> {phone}")
                    else:
                        print(f"   ⚠️ No phone found: {place.get('name')}")
                
                enriched.extend(batch)
                
                # Rate limiting
                await asyncio.sleep(1.5)
                
            except Exception as e:
                print(f"   ⚠️ Phone enrichment error: {e}")
                enriched.extend(batch)
        
        return enriched
    
    def _are_same_place(self, place1: Dict[str, Any], place2: Dict[str, Any]) -> bool:
        """Check if two places are the same business"""
        name1 = place1.get('name', '').lower().strip()
        name2 = place2.get('name', '').lower().strip()
        
        # Exact match
        if name1 == name2:
            return True
        
        # Substring match (for variations)
        if len(name1) > 5 and len(name2) > 5:
            if name1 in name2 or name2 in name1:
                return True
        
        return False
    
    def _filter_by_area(self, places: List[Dict[str, Any]], area: str) -> List[Dict[str, Any]]:
        """Filter places to only include those in the specified area"""
        filtered = []
        area_lower = area.lower().strip()
        
        # Handle variations
        area_variations = [
            area_lower,
            area_lower.replace(' ', ''),
            area_lower.replace(' ', '-'),
        ]
        
        for place in places:
            # Check address
            address = place.get('address', '').lower()
            name = place.get('name', '').lower()
            description = place.get('description', '').lower()
            
            # Check if area appears in any field
            if any(variation in address for variation in area_variations) or \
               any(variation in name for variation in area_variations) or \
               any(variation in description for variation in area_variations):
                filtered.append(place)
                print(f"   ✅ KEPT: {place.get('name')}")
            else:
                print(f"   ❌ FILTERED: {place.get('name')} (no '{area}' found)")
        
        return filtered
