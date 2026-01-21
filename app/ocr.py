import base64
import pytesseract
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def extract_text_from_image(base64_image: str):
    try:
        image_bytes = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        cv_img = np.array(image)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray).strip()

        if not text:
            return "", 0.0

        confidence = min(0.95, 0.6 + len(text) / 150)
        return text, round(confidence, 2)

    except Exception:
        return "", 0.0
