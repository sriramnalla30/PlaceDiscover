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
            print(f"Generated prompt: {prompt[:200]}...")
            response = await self._generate_response(prompt)
            print(f"Gemini response: {response[:300]}...")
            places = self._parse_response(response)
            print(f"Parsed places count: {len(places)}")
            return places
        except Exception as e:
            print(f"Error in Gemini search: {e}")
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
            
        prompt = f"""Find general information about {search_term} locations in {area}, {city}, India.

IMPORTANT: Instead of guessing specific business names, provide general location-based results.

Return a JSON array with 2-3 general location suggestions:

[
  {{
    "name": "{search_term.title()} near {area}",
    "address": "{area} area, {city}, India",
    "phone": "",
    "description": "Search for {search_term} in {area} area for current options and availability"
  }}
]

RULES:
- Use generic location-based names only
- NO specific business names unless you're 100% certain they exist
- Focus on area-based descriptions
- Let users find specific businesses through maps
- Provide general guidance rather than specific claims
- Return JSON only, no additional text

Search area: {area}, {city}"""
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
            for place_data in places_data[:8]:  # Limit to 8 places
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
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response}")
            return self._create_fallback_response()
        except Exception as e:
            print(f"Response parsing error: {e}")
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