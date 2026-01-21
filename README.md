\# AI-Powered Appointment Scheduler Assistant

\## Overview


This project is a backend service that converts natural language or document-based appointment requests into structured scheduling data.


It supports both typed text and image-based inputs and processes them through OCR, entity extraction, normalization, and guardrails to produce a final appointment JSON.

\## Features


\- Accepts typed text or image input

\- OCR support using Tesseract

\- Entity extraction (department, date phrase, time phrase)

\- Date and time normalization to Asia/Kolkata timezone

\- Guardrails for ambiguous or incomplete inputs

\- Clean, structured JSON responses

\## Tech Stack


\- Python 3.10+

\- FastAPI

\- Tesseract OCR

\- OpenCV

\- python-dateutil

\- pytz

\## Architecture Flow


Input (Text / Image)  

↓  

OCR / Text Extraction  

↓  

Entity Extraction  

↓  

Date \& Time Normalization (Asia/Kolkata)  

↓  

Guardrails  

↓  

Final Appointment JSON

\## Setup Instructions

\### 1. Clone the Repository

```bash

git clone <your-github-repo-url>

cd appointment-ai

\### 2. Create and Activate Virtual Environment

```bash

python -m venv venv

venv\\Scripts\\activate

```

\### 3. Install Dependencies

```bash

pip install -r requirements.txt

\### 4. Install Tesseract OCR (Windows)

\- Download and install Tesseract OCR from the official UB-Mannheim Windows build

\- Add the following path to System Environment Variables (PATH):

C:\\Program Files\\Tesseract-OCR\\

Verify installation:

```bash

tesseract --version

\### 5. Run the Application

```bash

uvicorn app.main:app --reload

```

Open Swagger UI in your browser:

```

http://127.0.0.1:8000/docs

```

\## API Endpoints

\### 1. Parse Appointment (OCR / Text Extraction)


\*\*Endpoint\*\*

```

POST /api/v1/appointment/parse

```

\*\*Request Body\*\*

```json

{

 "input_type": "text",

 "content": "Book dentist next Friday at 3pm"

}

```

\*\*Response\*\*

```json

{

 "raw_text": "Book dentist next Friday at 3pm",

 "confidence": 0.80

}

```

\### 2. Extract Appointment Entities

\*\*Endpoint\*\*

```

POST /api/v1/appointment/entities

```

\*\*Request Body\*\*

```json

{

 "input_type": "text",

 "content": "Book dentist next Friday at 3pm"

}

```

\*\*Response\*\*

```json

{

 "entities": {

   "department": "dentist",

   "date_phrase": "next Friday",

   "time_phrase": "3pm"

 },

 "entities_confidence": 0.85

}

```

\### 3. Normalize Date \& Time

\*\*Endpoint\*\*

```

POST /api/v1/appointment/normalize

```

\*\*Request Body\*\*

```json

{

 "date_phrase": "next Friday",

 "time_phrase": "3pm"

}

```

\*\*Response\*\*

```json

{

 "normalized": {

   "date": "YYYY-MM-DD",

   "time": "15:00",

   "tz": "Asia/Kolkata"

 },

 "normalization_confidence": 0.90

}

```

\### 4. Final Appointment Output

\*\*Endpoint\*\*

```
POST /api/v1/appointment/final

```

\*\*Request Body\*\*

```json

{

 "input_type": "text",

 "content": "Book dentist next Friday at 3pm"

}

```

\*\*Response\*\*

```json

{

 "appointment": {

   "department": "Dentistry",

   "date": "YYYY-MM-DD",

   "time":" 15:00"
 }

## Guardrails & Error Handling

```json
{
  "status": "needs_clarification",
  "message": "Ambiguous date/time or department"
}

```
\## STEP 6 — cURL \& Postman Requests

\### 6.1 Parse Appointment (OCR / Text Extraction)

```bash

curl -X POST http://127.0.0.1:8000/api/v1/appointment/parse \\

-H "Content-Type: application/json" \\

-d '{

 "input_type": "text",

 "content": "Book dentist next Friday at 3pm"

}'

{

 "raw_text": "Book dentist next Friday at 3pm",

 "confidence": 0.80

}

curl -X POST http://127.0.0.1:8000/api/v1/appointment/entities \\

-H "Content-Type: application/json" \\

-d '{

 "input_type": "text",

 "content": "Book dentist next Friday at 3pm"

}'

{

 "entities": {

   "department": "dentist",

   "date_phrase": "next Friday",

   "time_phrase": "3pm"

 },

 "entities_confidence": 0.85

}

curl -X POST http://127.0.0.1:8000/api/v1/appointment/normalize \\

-H "Content-Type: application/json" \\

-d '{

 "date_phrase": "next Friday",

 "time_phrase": "3pm"

}'

{

 "normalized": {

   "date": "YYYY-MM-DD",

   "time": "15:00",

   "tz": "Asia/Kolkata"

 },

 "normalization_confidence": 0.90

}

curl -X POST http://127.0.0.1:8000/api/v1/appointment/final \\

-H "Content-Type: application/json" \\

-d '{

 "input_type": "text",

 "content": "Book dentist next Friday at 3pm"

}'

{

 "appointment": {

   "department": "Dentist",

   "date": "YYYY-MM-DD",

   "time": "15:00",

   "tz": "Asia/Kolkata"

 },

 "status": "ok"

}



