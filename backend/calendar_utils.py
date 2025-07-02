# calendar_utils.py

from datetime import datetime, time, timedelta
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil import parser  # for parsing event time strings
import os


SCOPES = ['https://www.googleapis.com/auth/calendar']
import os, base64

# Decode service_account.json if it doesn't exist
if not os.path.exists("service_account.json"):
    encoded_key = os.getenv("SERVICE_ACCOUNT_B64")
    if encoded_key:
        with open("service_account.json", "wb") as f:
            f.write(base64.b64decode(encoded_key))

SERVICE_ACCOUNT_FILE = 'service_account.json'  # path to your credentials
CALENDAR_ID= "alfiyasimran05@gmail.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('calendar', 'v3', credentials=credentials)

def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'service_account.json'  # make sure path is correct

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('calendar', 'v3', credentials=credentials)
    return service

def get_free_slots(date_str: str):
    service = get_calendar_service()
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    tz = pytz.timezone("Asia/Kolkata")

    # Start and end of working day
    start_of_day = tz.localize(datetime.combine(date, time(9, 0)))
    end_of_day = tz.localize(datetime.combine(date, time(22, 0)))

    # Now
    now = datetime.now(tz)
    if date < now.date():
        return []
    # Fetch busy events
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    busy_slots = []
    for event in events_result.get("items", []):
        start = parser.isoparse(event["start"]["dateTime"])
        end = parser.isoparse(event["end"]["dateTime"])
        busy_slots.append((start, end))

    # Generate available 30-minute slots
    slot_duration = timedelta(minutes=30)
    current = start_of_day
    slots = []

    while current + slot_duration <= end_of_day:
        slot_start = current
        slot_end = current + slot_duration

        # ✅ Skip if this slot is in the past (only for today)
        if date == now.date() and slot_end <= now:
            current += slot_duration
            continue

        # ✅ Skip if overlaps with any busy slot
        if all(not (slot_start < b_end and slot_end > b_start) for b_start, b_end in busy_slots):
            slots.append((slot_start, slot_end))

        current += slot_duration

    return slots




def create_event(start_time: datetime, end_time: datetime, summary="Appointment with TailorBot"):
    """
    Creates an event in your calendar.
    """
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'}
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event.get('htmlLink')
