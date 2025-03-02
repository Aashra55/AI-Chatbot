import os
import streamlit as st 
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure API key
load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)

available_models = genai.list_models()

for model in available_models:
    print(model.name)

# Function to get response from Gemini
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

# Set up the page configuration
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

# Custom CSS for a black-themed, chat-like UI with a scrollable chat area
st.markdown("""
    <style>
        .stApp {
            background-color: black;
            color: white;
        }
                .stApp header{
            background: black
        }
        h1, h2, h3, h4, h5, h6, p{
            color: white
        }
.chat-container {
    margin: 0 auto;
    margin-bottom: 10px;
    height: calc(100vh - 220px); /* Reduced height to give more room at the bottom */
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #444;
    border-radius: 10px;
    background-color: #111;
}
        .message {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            animation: fadeIn 0.3s ease-in-out;
        }
        .user-message {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            text-align: right;
        }
        .bot-message {
            background: linear-gradient(135deg, #ffffff, #cccccc);
            color: black;
            text-align: left;
        }
        .input-container {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            max-width: 700px;
            width: 90%;
        }
        .stFormSubmitButton>button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            width: 10%;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Chatbot (Gemini)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Build the complete HTML for the chat container
html_chat = '<div class="chat-container">'
for message in st.session_state.messages:
    if message["role"] == "user":
        html_chat += f'<div class="message user-message">{message["content"]}</div>'
    else:
        html_chat += f'<div class="message bot-message">{message["content"]}</div>'
html_chat += '</div>'

# Render the chat container as one HTML block
st.markdown(html_chat, unsafe_allow_html=True)

# Fixed input container at the bottom using a form that clears on submit
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here...", key="chat_input")
        submit_button = st.form_submit_button("Send")
        if submit_button and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = chat_with_gemini(user_input)
            st.session_state.messages.append({"role": "bot", "content": response})
            st.rerun()


