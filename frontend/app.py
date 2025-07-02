# app.py

import streamlit as st
import requests
from datetime import datetime, time
import os
st.set_page_config(page_title="TailorBot - Calendar Booking", layout="centered")


def local_css(file_name):
    full_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(full_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")  # ✅ Keep as-is now that the function handles the path

st.title("TailorBot - Calendar Booking Assistant")
st.markdown("Chat with me to check availability and book appointments!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Backend URL (FastAPI, not Streamlit!)
API_URL = "https://tailorbot-backend.onrender.com/chat"

# 📅 Booking form
with st.expander("📅 Book a Slot Manually"):
    # Prevent past dates
    date = st.date_input("Select a Date", min_value=datetime.today().date())

    # Editable clock-like inputs with default values
    start_time = st.time_input(
        "Start Time", value=time(10, 0), help="Select or type the start time (HH:MM)"
    )
    end_time = st.time_input(
        "End Time", value=time(10, 30), help="Select or type the end time (HH:MM)"
    )

    if st.button("✅ Book This Slot"):
        message = f"Book a slot from {date} {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}"
        with st.spinner("TailorBot is checking..."):
            try:
                response = requests.post(API_URL, json={"message": message})
                result = response.json()["response"]
                if "confirmed" in result.lower():
                    st.success(result)
                else:
                    st.error(result)
            except Exception as e:
                st.error("❌ Could not connect to backend.")
                st.exception(e)
        

# 💬 Quick buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📅 Check Slots - 2025-07-05"):
        user_msg = "What slots are available on 2025-07-05?"
        st.session_state.messages.append({"role": "user", "content": user_msg})

        with st.spinner("TailorBot is thinking..."):
            try:
                response = requests.post(API_URL, json={"message": user_msg})
                bot_reply = response.json().get("response", "🤖 No response from bot.")
            except Exception as e:
                st.error("❌ Could not reach backend.")
                st.exception(e)
                bot_reply = "⚠️ Error getting response."

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

with col2:
    if st.button("🕒 Book Sample Slot"):
        user_msg = "Book a slot from 2025-07-05 11:00 to 11:30"
        st.session_state.messages.append({"role": "user", "content": user_msg})

        with st.spinner("TailorBot is thinking..."):
            try:
                response = requests.post(API_URL, json={"message": user_msg})
                bot_reply = response.json().get("response", "🤖 No response from bot.")
            except Exception as e:
                st.error("❌ Could not reach backend.")
                st.exception(e)
                bot_reply = "⚠️ Error getting response."

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})


# 💬 Chat input field
# 💬 Chat input field
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🔒 Always define result
    result = "⚠️ Something went wrong."

    with st.spinner("TailorBot is thinking..."):
        try:
            response = requests.post(API_URL, json={"message": user_input})
            if response.status_code == 200:
                result = response.json().get("response", "🤔 No response from agent.")
            else:
                result = f"❌ Backend returned {response.status_code}"
        except Exception as e:
            st.error("❌ Could not reach backend.")
            st.exception(e)

    st.session_state.messages.append({"role": "assistant", "content": result})



# 💬 Display chat messages with avatars
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
