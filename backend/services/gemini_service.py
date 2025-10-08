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
        Search for places using Gemini AI
        """
        try:
            prompt = self._create_search_prompt(city, area, place_type)
            print(f"\n{'='*50}")
            print(f"🔍 SEARCH REQUEST:")
            print(f"City: {city}")
            print(f"Area: {area}")
            print(f"Type: {place_type}")
            print(f"\n📝 FULL PROMPT SENT TO GEMINI:")
            print(prompt)
            print(f"{'='*50}")
            
            response = await self._generate_response(prompt)
            
            print(f"\n🤖 RAW GEMINI RESPONSE:")
            print(f"Response length: {len(response)} characters")
            print(f"Full response: {response}")
            print(f"{'='*50}")
            
            places = self._parse_response(response)
            
            print(f"\n✅ PARSED RESULTS:")
            print(f"Places found: {len(places)}")
            for i, place in enumerate(places):
                print(f"Place {i+1}:")
                print(f"  Name: {place.get('name', 'NO NAME')}")
                print(f"  Address: {place.get('address', 'NO ADDRESS')}")
                print(f"  Phone: {place.get('phone', 'NO PHONE')}")
                print(f"  Description: {place.get('description', 'NO DESCRIPTION')}")
            print(f"{'='*50}\n")
            
            return places
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
            print(f"\n🔧 PARSING GEMINI RESPONSE:")
            print(f"Original response length: {len(response)}")
            
            # Clean the response - remove markdown formatting if present
            cleaned_response = response.strip()
            print(f"After strip: '{cleaned_response[:100]}...'")
            
            if cleaned_response.startswith('```json'):
                cleaned_response = re.sub(r'^```json\s*', '', cleaned_response)
                print("Removed ```json prefix")
            if cleaned_response.endswith('```'):
                cleaned_response = re.sub(r'\s*```$', '', cleaned_response)
                print("Removed ``` suffix")
                
            print(f"Final cleaned response: {cleaned_response}")
            
            # Parse JSON
            print(f"Attempting to parse JSON...")
            places_data = json.loads(cleaned_response)
            print(f"JSON parsed successfully! Type: {type(places_data)}, Items: {len(places_data) if isinstance(places_data, list) else 'Not a list'}")
            
            # Validate and clean data
            places = []
            for i, place_data in enumerate(places_data[:8]):  # Limit to 8 places
                print(f"\nProcessing place {i+1}: {place_data}")
                if isinstance(place_data, dict) and 'name' in place_data:
                    place = {
                        'name': place_data.get('name', '').strip(),
                        'address': place_data.get('address', '').strip(),
                        'phone': self._clean_phone_number(place_data.get('phone', '')),
                        'description': place_data.get('description', '').strip()
                    }
                    
                    print(f"Created place object: {place}")
                    
                    # Validate place data quality
                    if self._is_valid_place(place):
                        places.append(place)
                        print(f"✅ Place {i+1} is valid and added")
                    else:
                        print(f"❌ Place {i+1} failed validation")
                else:
                    print(f"❌ Place {i+1} is not a valid dict or missing name")
            
            print(f"Final places list: {len(places)} valid places")
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