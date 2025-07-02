# 👕 TailorBot – Calendar Booking Assistant

TailorBot is a conversational AI assistant that helps users book appointments on their Google Calendar — either via chat or a manual form.

## 🚀 Features

- 💬 Conversational interface (LLM-powered)
- 🗕️ Manual slot picker (date + time)
- ✅ Checks real-time availability
- 🔗 Google Calendar (Service Account)
- 🎨 Streamlit frontend, FastAPI backend
- 🔒 Secure service account handling via env

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM**: Groq via LangChain
- **Calendar**: Google Calendar API
- **Hosting**: Render (backend), Streamlit Cloud (frontend)

## 🔐 ENV Setup

On both platforms, set:

```bash
SERVICE_ACCOUNT_B64 = "<base64-encoded-service-account.json>"
```

Backend decodes it using:

```python
import base64, os, json
from google.oauth2 import service_account

creds = json.loads(base64.b64decode(os.getenv("SERVICE_ACCOUNT_B64")).decode())
credentials = service_account.Credentials.from_service_account_info(creds)
```

## 📂 Structure

```
tailorbot/
├── backend/
│   ├── main.py
│   ├── agent.py
│   └── calendar_utils.py
├── frontend/
│   ├── app.py
│   └── styles.css
```

## 🔗 Live Links

- 🌐 **Frontend**: [Streamlit](https://tailorbot-frontend.streamlit.app)
- ⚙️ **Backend**: [Render](https://tailorbot-backend.onrender.com/chat)
- 💻 **GitHub**: [github.com/Alfiya-Simran/tailorbot](https://github.com/Alfiya-Simran/tailorbot)

## 👩‍💻 Developer

**Alfiya Simran**  
📧 alfiya.simran05@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/alfiya-simran)

