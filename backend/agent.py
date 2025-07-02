# agent.py

import os
from groq import Groq
from dotenv import load_dotenv
from backend.calendar_utils import get_free_slots, create_event
from datetime import datetime
import pytz

load_dotenv()

# ✅ Groq API client (direct call, no langchain needed)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqBot:
    def invoke(self, message):
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You're TailorBot, a helpful assistant for managing calendar bookings."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()

llm = GroqBot()


# Tools still available for future use
def available_slots_tool(date_str: str):
    slots = get_free_slots(date_str)

    if not slots:
        return f"❌ No available slots found on {date_str}."

    return (
        f"✅ Available slots on {date_str}:\n\n" +
        "\n".join([f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}" for s, e in slots])
    )


def book_slot_tool(start: str, end: str):
    tz = pytz.timezone('Asia/Kolkata')
    start_dt = tz.localize(datetime.strptime(start, "%Y-%m-%d %H:%M"))
    end_dt = tz.localize(datetime.strptime(end, "%Y-%m-%d %H:%M"))

    now = datetime.now(tz)
    if start_dt < now:
        return "❌ You can't book a slot in the past. Please choose a future time."

    return create_event(start_dt, end_dt)

