from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import AppointmentInput, OCRResponse, EntityResponse
from app.ocr import extract_text_from_image
from app.entity_extractor import extract_entities
from app.services.normalization import normalize_datetime

router = APIRouter(prefix="/api/v1")


# ---------- STEP 1: OCR / TEXT EXTRACTION ----------
@router.post("/appointment/parse", response_model=OCRResponse)
def parse_appointment(data: AppointmentInput):

    if data.input_type == "text":
        raw_text = data.content.strip()
        confidence = min(0.95, 0.6 + len(raw_text) / 150)

    elif data.input_type == "image":
        raw_text, confidence = extract_text_from_image(data.content)
        if not raw_text:
            raise HTTPException(400, "OCR failed")

    else:
        raise HTTPException(400, "Invalid input_type")

    return {
        "raw_text": raw_text,
        "confidence": round(confidence, 2)
    }


# ---------- STEP 2: ENTITY EXTRACTION ----------
@router.post("/appointment/entities", response_model=EntityResponse)
def extract_appointment_entities(data: AppointmentInput):

    if not data.content.strip():
        raise HTTPException(400, "Empty content")

    return extract_entities(data.content)


# ---------- STEP 3: NORMALIZATION ----------
class NormalizeInput(BaseModel):
    date_phrase: str
    time_phrase: str


@router.post("/appointment/normalize")
def normalize_appointment(input: NormalizeInput):

    result = normalize_datetime(
        input.date_phrase,
        input.time_phrase
    )

    if not result:
        return {
            "status": "needs_clarification",
            "message": "Ambiguous date/time or department"
        }

    return {
        "normalized": result,
        "normalization_confidence": 0.9
    }
# ---------- STEP 4: FINAL APPOINTMENT PIPELINE ----------
@router.post("/appointment/final")
def final_appointment(data: AppointmentInput):

    # Step 1: OCR / Text
    if data.input_type == "text":
        raw_text = data.content.strip()
    elif data.input_type == "image":
        raw_text, _ = extract_text_from_image(data.content)
        if not raw_text:
            return {
                "status": "needs_clarification",
                "message": "Unable to read image clearly"
            }
    else:
        return {
            "status": "needs_clarification",
            "message": "Invalid input type"
        }

    # Step 2: Entity Extraction
    entity_result = extract_entities(raw_text)
    entities = entity_result["entities"]

    if not entities["department"] or not entities["date_phrase"] or not entities["time_phrase"]:
        return {
            "status": "needs_clarification",
            "message": "Ambiguous date/time or department"
        }

    # Step 3: Normalization
    normalized = normalize_datetime(
        entities["date_phrase"],
        entities["time_phrase"]
    )

    if not normalized:
        return {
            "status": "needs_clarification",
            "message": "Ambiguous date/time or department"
        }

    return {
        "appointment": {
            "department": entities["department"].capitalize(),
            "date": normalized["date"],
            "time": normalized["time"],
            "tz": normalized["tz"]
        },
        "status": "ok"
    }
