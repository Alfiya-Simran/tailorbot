# 🤖 TailorBot – Calendar Booking Assistant

TailorBot is a conversational AI assistant that helps users check availability and book appointments directly on a connected Google Calendar — via chat or a manual form.

## ✨ Features

- 💬 Chat-based booking with natural language
- 📅 Manual booking form with date/time picker
- ✅ Google Calendar integration (via Service Account)
- 🎯 Real-time availability checks
- 🔒 Secure credential handling using environment variables
- 🖥️ Clean and intuitive Streamlit frontend

---

## 🛠️ Tech Stack

| Layer     | Technology       |
|-----------|------------------|
| Backend   | FastAPI          |
| Agent     | Langchain + Groq |
| Frontend  | Streamlit        |
| Calendar  | Google Calendar API (Service Account) |
| Hosting   | Render (Backend), Streamlit Cloud (Frontend) |

---

## 🚀 How It Works

1. **Conversational Agent**: Powered by Groq + LangChain to understand natural language.
2. **Google Calendar**: Authenticated using a Service Account for secure access.
3. **Slot Detection**: Checks for free 30-min blocks between 9 AM – 10 PM (IST).
4. **Booking**: Creates a new event on the calendar with user-defined details.
5. **Frontend UI**: Users can interact via chat or use manual booking form.

---

## 📂 Project Structure

```bash
tailorbot/
├── backend/
  ├── main.py # FastAPI app
  ├── agent.py # LLM + tool routing
  ├── calendar_utils.py # Google Calendar tools
  └── service_account.json # 🔒 (encoded in ENV)
├── frontend/
  ├── app.py # Streamlit interface
  └── styles.css # Basic UI styling
├── requirements.txt
├── README.md
```

---

## 🔐 Environment Variables

Make sure to set the following environment variable in both frontend and backend:

```bash
SERVICE_ACCOUNT_B64="your_base64_encoded_service_account.json"
```

In backend, decode it like this:

```bash
import base64, os, json
from google.oauth2 import service_account

service_account_info = json.loads(
    base64.b64decode(os.getenv("SERVICE_ACCOUNT_B64")).decode()
)
credentials = service_account.Credentials.from_service_account_info(service_account_info)
```

---

## 🔗 Live Links
🌐 **Frontend**: [Streamlit](https://tailorbot-frontend.streamlit.app)

⚙️ **Backend**: [Render](https://tailorbot-backend.onrender.com/chat)

💻 **GitHub**: [github.com/Alfiya-Simran/tailorbot](https://github.com/Alfiya-Simran/tailorbot)

---

## 🧠 Powered By
- LangChain
- Groq API
- Streamlit
- FastAPI
- Google Calendar API

---

## 📬 Contact
Developed by Alfiya Simran
📧 Email: alfiya.simran05@gmail.com
