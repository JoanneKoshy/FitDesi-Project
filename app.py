import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Fetch Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("🚨 GROQ_API_KEY is not set. Please check your .env file!")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit app config
st.set_page_config(page_title="FitDesi Buddy 🏋️🥗", page_icon="🇮🇳")
st.title("FitDesi Buddy")

# Sidebar controls
st.sidebar.header("⚙️ Settings")
desi_mode = st.sidebar.toggle("Desi Diet Mode 🇮🇳", value=True)

# Chat UI setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Tell me your fitness goal (e.g., lose weight, gain muscle, eat healthy)..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construct system prompt
    system_message = "You are FitDesi Buddy, a fitness & diet assistant. Provide workouts and meal plans." 
    if desi_mode:
        system_message += " Focus on Indian meals like roti, dal, sabzi, idli, dosa, poha, paneer, curd rice instead of western food."

    # Prepare conversation
    conversation = [{"role": "system", "content": system_message}] + st.session_state.messages

    # Get response from Groq
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Available Groq LLaMA model
        messages=conversation,
        temperature=0.7,
    )

    reply = response.choices[0].message.content

    # Save and display reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
