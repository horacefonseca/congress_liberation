"""Search utilities for Congress Connect"""

from typing import Optional, Dict, List
from utils.database import CongressDatabase
from utils.api_clients import GoogleCivicAPI


def search_by_zip(zip_code: str, db: CongressDatabase, google_api: GoogleCivicAPI = None) -> Dict:
    """
    Search for representatives by ZIP code
    Returns: {
        "success": bool,
        "district": str or None,
        "house_rep": dict or None,
        "senators": list,
        "message": str
    }
    """
    result = {
        "success": False,
        "district": None,
        "house_rep": None,
        "senators": [],
        "message": ""
    }

    # Validate ZIP code
    if not zip_code or len(zip_code) != 5 or not zip_code.isdigit():
        result["message"] = "Please enter a valid 5-digit ZIP code"
        return result

    # Try to get district from ZIP (using API or fallback)
    if google_api:
        district_info = google_api.get_district_from_zip(zip_code)
    else:
        district_info = manual_zip_to_district(zip_code)

    if not district_info:
        result["message"] = "Could not determine district. Please select manually."
        return result

    district = district_info.get("district")
    state = district_info.get("state", "FL")

    # Get house representative
    house_rep = db.get_representative_by_district(district)

    # Get senators
    senators = db.get_senators_by_state(state)

    if house_rep or senators:
        result["success"] = True
        result["district"] = district
        result["house_rep"] = house_rep
        result["senators"] = senators
        result["message"] = f"Found representatives for {district}"
    else:
        result["message"] = f"No representatives found for {district}"

    return result


def search_by_district(district: str, db: CongressDatabase) -> Optional[Dict]:
    """Search for representative by district code"""
    return db.get_representative_by_district(district)


def get_all_florida_reps(db: CongressDatabase) -> List[Dict]:
    """Get all Florida representatives"""
    return db.get_all_representatives(state='FL')


def manual_zip_to_district(zip_code: str) -> Optional[Dict]:
    """
    Manual ZIP to district mapping for Florida
    This is a simplified fallback - would need complete database for production
    """
    zip_int = int(zip_code)

    # Sample mappings (would need complete data)
    mappings = {
        range(32004, 32100): "FL-04",  # Jacksonville area
        range(32301, 32400): "FL-02",  # Tallahassee
        range(32601, 32700): "FL-03",  # Gainesville
        range(33101, 33200): "FL-27",  # Miami
        range(33301, 33400): "FL-23",  # Fort Lauderdale
        range(33401, 33500): "FL-22",  # West Palm Beach
        range(33601, 33700): "FL-14",  # Tampa
        range(33701, 33800): "FL-13",  # St. Petersburg
        range(33901, 34000): "FL-19",  # Fort Myers/Naples area
        range(34101, 34200): "FL-25",  # Collier County
    }

    for zip_range, district in mappings.items():
        if zip_int in zip_range:
            return {"district": district, "state": "FL"}

    return None
