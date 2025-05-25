from app.mappings.field_mappings import GLOBAL_TRUST_MAPPING
from app.models.schemas import ProcessedTrustResponse

def compare_trust_responses(response1: ProcessedTrustResponse, response2: ProcessedTrustResponse) -> dict:
    """
    Compare two trust document responses using the global field mapping
    """
    comparison = {}
    
    for field, display_name in GLOBAL_TRUST_MAPPING.items():
        value1 = getattr(response1.data, field, None)
        value2 = getattr(response2.data, field, None)
        
        # Special handling for list comparisons
        if isinstance(value1, list) and isinstance(value2, list):
            is_match = sorted(value1) == sorted(value2)
        else:
            is_match = value1 == value2
        
        comparison[display_name] = {
            "status": "match" if is_match else "mismatch",
            "value1": value1,
            "value2": value2,
            "required": field not in ['unit_holders']  # All fields except unit_holders are required
        }
    
    # Calculate match statistics
    required_fields = [f for f in comparison.values() if f["required"]]
    matching_fields = sum(1 for f in comparison.values() if f["status"] == "match")
    required_matches = sum(1 for f in required_fields if f["status"] == "match")
    
    comparison["summary"] = {
        "total_fields": len(comparison),
        "matching_fields": matching_fields,
        "required_fields_matched": required_matches,
        "total_required_fields": len(required_fields),
        "match_percentage": int((required_matches / len(required_fields)) * 100) if required_fields else 0,
        "status": "Complete Match" if required_matches == len(required_fields) else 
                 "Partial Match" if required_matches > 0 else 
                 "No Match"
    }
    
    return comparison