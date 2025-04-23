# app/services/comparison_service.py
from typing import Dict, List
from app.models.schemas import ProcessedResponse
from app.utils.helpers import values_match, get_overall_status, normalize_value
from app.mappings.field_mappings import EXPECTED_FIELDS

def compare_responses(responses: List[ProcessedResponse]) -> Dict:
    """
    Compare multiple response dictionaries and return a detailed comparison result.
    Uses the Levenshtein algorithm with field-specific thresholds for specific fields and exact matching for others.
    """
    common_fields = EXPECTED_FIELDS
    matching_fields = {}
    mismatched_fields = {}
    
    # Fields to use Levenshtein algorithm for, with specific thresholds
    levenshtein_fields_thresholds = {
        "Company Name": 0.9,
        "Bank Bureau Name": 0.9,
        "Amount Limit in Words": 0.7,
        "Period Ending": 0.75,
        "Drawing Account Name": 0.85,
        "Limit Frequency": 0.70
    }

    for field, ui in common_fields.items():
        # Collect all available values for this field
        values = [
            response.data.get(field) for response in responses
            if field in response.data and response.data.get(field) is not None
        ]

        if not values:
            continue

        # Determine if the field should use Levenshtein or exact matching
        if ui in levenshtein_fields_thresholds:
            # Use Levenshtein algorithm for specific fields with field-specific threshold
            threshold = levenshtein_fields_thresholds[ui]
            is_match = True
            for i in range(1, len(values)):
                if not values_match(values[0], values[i], threshold):
                    is_match = False
                    break
        else:
            # Use exact matching for other fields
            # Normalize all values before comparison
            normalized_values = [normalize_value(value) for value in values]
            is_match = all(value == normalized_values[0] for value in normalized_values)

        if is_match:
            # If values match, store all original values and mark as a match
            matching_fields[ui] = {
                "values": values,  # Store all original values
                "status": "match"  # Mark as a match
            }
        else:
            # If values do not match, store all original values and mark as a mismatch
            mismatched_fields[ui] = {
                "values": values,  # Store all original values
                "status": "mismatch"  # Mark as a mismatch
            }

    overall_status = get_overall_status(len(matching_fields), len(common_fields))

    return {
        "status": overall_status,
        "matching_fields": matching_fields,
        "mismatched_fields": mismatched_fields,
        "document_types": [response.document_type for response in responses],
        "normalized_matches": {
            field: {
                "original_values": values,
                "normalized_value": normalize_value(values)  # Normalize the first value for display
            }
            for field, values in matching_fields.items()
        }
    }