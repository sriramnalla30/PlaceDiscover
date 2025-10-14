"""
SerpStack Service - Real Google SERP data for accurate place search
Uses SerpStack API to get actual Google search results with local data
"""
import requests
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

class SerpStackService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("SERPSTACK_API_KEY", "088f24b4864557232354176ec84fceb7")
        self.base_url = "http://api.serpstack.com/search"
    
    def search_places(self, city: str, area: str, place_type: str) -> List[Dict[str, Any]]:
        """
        Search for places using SerpStack (Real Google SERP data)
        Returns actual businesses from Google search results
        """
        try:
            # Build search query
            query = f"{place_type} in {area}, {city}"
            
            print(f"\n{'='*80}")
            print(f"🔍 SERPSTACK SEARCH")
            print(f"📍 Query: {query}")
            print(f"{'='*80}\n")
            
            # Make API request
            params = {
                'access_key': self.api_key,
                'query': query,
                'location': f"{area}, {city}, India",  # Geo-targeted search
                'google_domain': 'google.co.in',  # Indian Google
                'gl': 'in',  # India country code
                'hl': 'en',  # English language
                'num': 10  # Number of results
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ SerpStack API error: {response.status_code}")
                print(f"Response: {response.text}")
                return []
            
            data = response.json()
            
            # Check for API errors
            if not data.get('request', {}).get('success', False):
                error = data.get('error', {})
                print(f"❌ SerpStack error: {error.get('info', 'Unknown error')}")
                return []
            
            print(f"✅ SerpStack request successful!")
            
            # Extract results
            results = []
            
            # PRIORITY 1: Extract phone numbers from related_places first
            related_places = data.get('related_places', [])
            phone_map = {}
            
            if related_places:
                import re
                print(f"\n📞 Extracting phone numbers from related_places...")
                for place in related_places:
                    place_text = place.get('places', '')
                    title = place.get('title', '')
                    
                    # Extract phone number using regex (Indian format)
                    # Matches: 092990 50505, 072073 31335, 095780 01111
                    phone_match = re.search(r'(\d{5}\s?\d{5}|\d{10})', place_text)
                    if phone_match:
                        phone = phone_match.group(1).replace(' ', '')
                        phone_map[title] = phone
                        print(f"   📞 {title}: {phone}")
            
            # PRIORITY 2: Local Results (Best for location-specific searches)
            local_results = data.get('local_results', [])
            if local_results:
                print(f"\n📍 Found {len(local_results)} local results")
                for local in local_results:
                    business_name = local.get('title', '')
                    
                    # Get phone number from phone_map
                    phone = phone_map.get(business_name, '')
                    
                    # Build description from extensions
                    extensions = local.get('extensions', [])
                    description = f"Local result from Google Maps."
                    if extensions:
                        description += f" {', '.join(extensions[:2])}"
                    
                    place = {
                        'name': business_name,
                        'address': local.get('address', ''),
                        'phone': phone,
                        'description': description,
                        'source': 'SerpStack (Google Local)',
                        'rating': local.get('rating'),
                        'reviews': local.get('reviews'),
                        'url': local.get('url', '')
                    }
                    
                    results.append(place)
                    phone_display = f"📞 {phone}" if phone else "No phone"
                    print(f"   ✅ {place['name']} | {phone_display}")
            
            # PRIORITY 2: Organic Results (Only if we need more results)
            # Skip generic directory listings (JustDial, Sulekha, etc.)
            organic_results = data.get('organic_results', [])
            if organic_results and len(results) < 3:  # Only add if we have less than 3 local results
                print(f"\n🌐 Found {len(organic_results)} organic results")
                
                # Filter out directory websites
                directory_domains = [
                    'justdial.com',
                    'sulekha.com',
                    'gympik.com',
                    'zomato.com',
                    'magicbricks.com',
                    'yellow-pages.com',
                    '99acres.com',
                    'timesnow.com',
                    'indiamart.com',
                    'tradeindia.com'
                ]
                
                for organic in organic_results[:6 - len(results)]:
                    url = organic.get('url', '').lower()
                    
                    # Skip if it's a directory listing
                    if any(domain in url for domain in directory_domains):
                        print(f"   ⏭️  Skipped directory: {organic.get('title', '')[:50]}...")
                        continue
                    
                    # Extract rating and reviews from rich snippet
                    rich_snippet = organic.get('rich_snippet', {})
                    rating = None
                    reviews = None
                    
                    for location in ['top', 'bottom']:
                        if location in rich_snippet:
                            detected = rich_snippet[location].get('detected_extensions', {})
                            rating = detected.get('rating')
                            reviews = detected.get('reviews') or detected.get('votes')
                            break
                    
                    place = {
                        'name': organic.get('title', ''),
                        'address': organic.get('displayed_url', ''),
                        'phone': '',  # Organic results usually don't have phone
                        'description': organic.get('snippet', '')[:200],
                        'source': 'SerpStack (Google Organic)',
                        'rating': rating,
                        'reviews': reviews,
                        'url': organic.get('url', '')
                    }
                    
                    results.append(place)
                    print(f"   ✅ {place['name']}")
            
            print(f"\n✅ Total results: {len(results)}")
            print(f"{'='*80}\n")
            
            return results[:6]
            
        except requests.Timeout:
            print("❌ SerpStack API timeout")
            return []
        except Exception as e:
            print(f"❌ SerpStack error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get API usage statistics (optional)
        """
        try:
            # Note: SerpStack doesn't have a dedicated usage endpoint
            # Usage is tracked in the dashboard
            return {
                'message': 'Check dashboard at https://serpstack.com/dashboard',
                'free_tier': '100 requests/month'
            }
        except Exception as e:
            return {'error': str(e)}
