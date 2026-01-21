from datetime import datetime, timedelta
import pytz
from dateutil import parser

IST = pytz.timezone("Asia/Kolkata")

def normalize_datetime(date_phrase: str, time_phrase: str):
    try:
        now = datetime.now(IST)

        # Handle common phrase: "next Friday"
        if "next friday" in date_phrase.lower():
            days_ahead = (4 - now.weekday() + 7) % 7
            days_ahead = 7 if days_ahead == 0 else days_ahead
            date = now + timedelta(days=days_ahead)
        else:
            return None

        parsed_time = parser.parse(time_phrase)
        date = date.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0
        )

        return {
            "date": date.strftime("%Y-%m-%d"),
            "time": date.strftime("%H:%M"),
            "tz": "Asia/Kolkata"
        }

    except Exception:
        return None
