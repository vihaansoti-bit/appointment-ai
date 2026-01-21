import re

DEPARTMENTS = {
    "dentist": "Dentistry",
    "doctor": "General Medicine",
    "cardiologist": "Cardiology",
    "orthopedic": "Orthopedics"
}

TIME_REGEX = r"\b(\d{1,2}(:\d{2})?\s?(am|pm))\b"
DATE_PATTERNS = [
    r"(next\s+\w+)",
    r"(today)",
    r"(tomorrow)",
    r"(this\s+\w+)"
]

def extract_entities(text: str):
    text_lower = text.lower()

    # Department extraction
    department = None
    for key in DEPARTMENTS:
        if key in text_lower:
            department = key
            break

    # Time extraction
    time_match = re.search(TIME_REGEX, text_lower)
    time_phrase = time_match.group(0) if time_match else None

    # Date extraction
    date_phrase = None
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            date_phrase = match.group(0)
            break

    confidence = 0.85 if department and time_phrase and date_phrase else 0.6

    return {
        "entities": {
            "department": department,
            "date_phrase": date_phrase,
            "time_phrase": time_phrase
        },
        "entities_confidence": confidence
    }
