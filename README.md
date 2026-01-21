# AI-Powered Appointment Scheduler Assistant

## Overview
This project is a backend service that converts natural language or document-based appointment requests into structured scheduling data.

It supports both typed text and image-based inputs and processes them through OCR, entity extraction, normalization, and guardrails to produce a final appointment JSON.

---

## Features
- Accepts typed text or image input
- OCR support using Tesseract
- Entity extraction (department, date phrase, time phrase)
- Date and time normalization to Asia/Kolkata timezone
- Guardrails for ambiguous or incomplete inputs
- Clean, structured JSON responses

---

## Tech Stack
- Python 3.10+
- FastAPI
- Tesseract OCR
- OpenCV
- python-dateutil
- pytz

---

## Architecture Flow

Input (Text / Image)  
↓  
OCR / Text Extraction  
↓  
Entity Extraction  
↓  
Date & Time Normalization (Asia/Kolkata)  
↓  
Guardrails  
↓  
Final Appointment JSON  

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd appointment-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
C:\Program Files\Tesseract-OCR\
tesseract --version
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
{
  "input_type": "text",
  "content": "Book dentist next Friday at 3pm"
}
{
  "raw_text": "Book dentist next Friday at 3pm",
  "confidence": 0.80
}
{
  "input_type": "text",
  "content": "Book dentist next Friday at 3pm"
}
{
  "entities": {
    "department": "dentist",
    "date_phrase": "next Friday",
    "time_phrase": "3pm"
  },
  "entities_confidence": 0.85
}
{
  "date_phrase": "next Friday",
  "time_phrase": "3pm"
}
{
  "normalized": {
    "date": "YYYY-MM-DD",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "normalization_confidence": 0.90
}
{
  "input_type": "text",
  "content": "Book dentist next Friday at 3pm"
}
{
  "appointment": {
    "department": "Dentistry",
    "date": "YYYY-MM-DD",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}
{
  "status": "needs_clarification",
  "message": "Ambiguous date/time or department"
}
curl -X POST http://127.0.0.1:8000/api/v1/appointment/parse \
-H "Content-Type: application/json" \
-d '{
  "input_type": "text",
  "content": "Book dentist next Friday at 3pm"
}'
curl -X POST http://127.0.0.1:8000/api/v1/appointment/final \
-H "Content-Type: application/json" \
-d '{
  "input_type": "text",
  "content": "Book dentist next Friday at 3pm"
}'


