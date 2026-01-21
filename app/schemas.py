from pydantic import BaseModel
from typing import Optional

class AppointmentInput(BaseModel):
    input_type: str
    content: str

class OCRResponse(BaseModel):
    raw_text: str
    confidence: float

class EntityResponse(BaseModel):
    entities: dict
    entities_confidence: float
