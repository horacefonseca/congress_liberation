"""API clients for Congress Connect"""

import requests
from typing import Optional, Dict

class GoogleCivicAPI:
    """Client for Google Civic Information API"""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/civicinfo/v2/representatives"

    def get_district_from_zip(self, zip_code: str) -> Optional[Dict]:
        """
        Get congressional district from ZIP code
        Returns: {"district": "FL-27", "state": "FL"} or None
        """
        if not self.api_key:
            # Fallback: basic ZIP to district mapping for Florida
            return self._fallback_zip_lookup(zip_code)

        try:
            params = {
                "address": zip_code,
                "key": self.api_key,
                "levels": "country",
                "roles": ["legislatorLowerBody", "legislatorUpperBody"]
            }

            response = requests.get(self.base_url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                # Parse response to extract district
                # Implementation would parse the actual response
                return self._parse_civic_response(data)

        except Exception as e:
            print(f"API Error: {e}")
            return self._fallback_zip_lookup(zip_code)

        return None

    def _parse_civic_response(self, data: Dict) -> Optional[Dict]:
        """Parse Google Civic API response"""
        # Simplified parser - would need full implementation
        try:
            offices = data.get('offices', [])
            for office in offices:
                if 'U.S. House' in office.get('name', ''):
                    # Extract district info
                    division_id = office.get('divisionId', '')
                    if '/cd:' in division_id:
                        parts = division_id.split(':')
                        state_district = parts[-1]
                        state = state_district[:2].upper()
                        district_num = state_district[2:]
                        return {
                            "district": f"{state}-{district_num.zfill(2)}",
                            "state": state
                        }
        except:
            pass
        return None

    def _fallback_zip_lookup(self, zip_code: str) -> Optional[Dict]:
        """
        Simple fallback ZIP to district mapping for Florida
        NOTE: This is a simplified version. Full implementation would use comprehensive database
        """
        # Basic Florida ZIP ranges (simplified)
        zip_int = int(zip_code)

        # This is just sample data - would need complete mapping
        if 32004 <= zip_int <= 32099:
            return {"district": "FL-04", "state": "FL"}
        elif 33101 <= zip_int <= 33299:
            return {"district": "FL-27", "state": "FL"}
        elif 33301 <= zip_int <= 33499:
            return {"district": "FL-23", "state": "FL"}
        # Add more mappings...

        # Default to asking user to select district
        return None


class ProPublicaAPI:
    """Client for ProPublica Congress API"""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.base_url = "https://api.propublica.org/congress/v1"

    def get_recent_votes(self, bioguide_id: str, limit: int = 3) -> list:
        """Get recent votes for a representative"""
        if not self.api_key:
            return []

        try:
            url = f"{self.base_url}/members/{bioguide_id}/votes.json"
            headers = {"X-API-Key": self.api_key}

            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                votes = data.get('results', [{}])[0].get('votes', [])
                return votes[:limit]

        except Exception as e:
            print(f"ProPublica API Error: {e}")

        return []
