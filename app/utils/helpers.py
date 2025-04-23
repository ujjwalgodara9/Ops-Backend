# app/utils/helpers.py
import base64
import io
import PIL.Image
from fastapi import HTTPException
from Levenshtein import ratio as levenshtein_ratio

def base64_to_image(base64_str: str) -> PIL.Image.Image:
    """Convert a base64-encoded string to a PIL image."""
    try:
        image_data = base64.b64decode(base64_str)
        return PIL.Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(e)}")

def clean_base64(data: str) -> str:
    """Handle data URI prefix if present"""
    if data.startswith("data:image"):
        return data.split(",", 1)[1]
    return data

def normalize_value(value: str) -> str:
    """
    Normalize values by removing special characters, standardizing format,
    and handling None values.
    """
    if value is None:
        return "none"  # Normalize None to "none"

    if not isinstance(value, str):
        value = str(value)
    
    # Remove special characters, spaces, and convert to lowercase
    normalized = ''.join(char for char in value if char.isalnum()).lower()
    
    return normalized

def values_match(value1: str, value2: str, threshold: float = 0.8) -> bool:
    """
    Compare two values using the Levenshtein algorithm.
    If the similarity ratio is above the threshold, consider them a match.
    """
    # Normalize the values
    normalized_value1 = normalize_value(value1)
    normalized_value2 = normalize_value(value2)

    # Calculate the Levenshtein similarity ratio
    similarity_ratio = levenshtein_ratio(normalized_value1, normalized_value2)

    # Check if the similarity ratio meets the threshold
    return similarity_ratio >= threshold

def get_overall_status(matching_count: int, total_fields: int) -> str:
    """Determine the overall match status based on matching field count."""
    if matching_count == total_fields:
        return "Complete Match"
    elif matching_count > 0:
        return "Partial Match"
    return "No Match"