# main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import llm, available_slots_tool, book_slot_tool
from fastapi.middleware.cors import CORSMiddleware
import re
app = FastAPI()

# Enable CORS so your Streamlit frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:8501"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class UserMessage(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "TailorBot backend is live!"}


@app.post("/chat")
async def chat_with_bot(request: UserMessage):
  

    prompt = request.message.lower()
    response = "🤔 Sorry, I couldn't understand that."

    try:
        if prompt in ["hello", "hi", "hey"]:
            response = (
                "Hello there! I'm TailorBot, your go-to assistant for managing calendar bookings. "
                "I'm here to help you stay organized and on top of your schedule.\n\n"
                "What can I assist you with today? Do you need to:\n\n"
                "• Schedule a new booking?\n"
                "• View or edit an existing booking?\n"
                "• Check your availability for a specific date and time?\n"
                "• Something else?\n\n"
                "Let me know, and I'll be happy to help!"
            )

        # 🟦 Check availability intent
        if "available" in prompt or "slots" in prompt or "free time" in prompt:
            date_match = re.search(r"\d{4}-\d{2}-\d{2}", prompt)
            if date_match:
                date_str = date_match.group()
                response = available_slots_tool(date_str)
            else:
                response = "🗓️ Please provide a date in YYYY-MM-DD format to check available slots."

        # 🟩 Booking intent
        elif "book" in prompt and "from" in prompt and "to" in prompt:
            start_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", prompt)
            end_time_match = re.search(r"to (\d{2}:\d{2})", prompt)

            if start_match and end_time_match:
                start = start_match.group()
                date_part = start.split(" ")[0]
                end = f"{date_part} {end_time_match.group(1)}"
                response = book_slot_tool(start, end)
            else:
                response = "🕒 Please provide both start and end time in format YYYY-MM-DD HH:MM."

        # 🧠 Default to LLM agent
        else:
            response = llm.invoke(prompt)

    except Exception as e:
        print("❌ Agent error:", e)
        response = f"Error: {str(e)}"

    return {"response": response}



