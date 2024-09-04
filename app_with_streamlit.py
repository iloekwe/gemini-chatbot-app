import os
from dotenv import load_dotenv
import google.generativeai as genai
# import genai
import streamlit as st

# Load the environment variables from the .env file
load_dotenv()

# Access the API key from the environment
api_key = os.getenv['GEMINI_API_KEY']
# api_key = os.environ['GEMINI_API_KEY']

# Validate the API key
if not api_key:
    st.error("API key for GEMINI_API_KEY not found. Please set it in the .env file.")
    st.stop()

# Configure the genai module with the API key
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure genai: {e}")
    st.stop()

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

# Function to process input text
def process_text(input_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"You are a travel guide providing detailed information about various destinations around the world. {input_text}"
        response = model.generate_content(prompt)
        return response.text  # Adjust based on actual genai response structure
    except Exception as e:
        return f"Error generating response: {e}"

# Set page configuration
st.set_page_config(
    page_title="World Travel Guide Chat: Journey with Gemini",
    page_icon=":sparkles:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for a cosmic theme
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    .main-title {
        color: #e0e0e0;
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 0px 0px 8px #fff;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { text-shadow: 0 0 5px #ffffff, 0 0 10px #ffffff, 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff0000, 0 0 55px #ff0000, 0 0 75px #ff0000; }
        100% { text-shadow: 0 0 5px #ffffff, 0 0 10px #ff4b4b, 0 0 20px #ff4b4b, 0 0 30px #ff4b4b, 0 0 40px #ff4b4b, 0 0 55px #ff4b4b, 0 0 75px #ff4b4b; }
    }
    .input-box {
        border: 2px solid #ff4b4b;
        padding: 10px;
        border-radius: 10px;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    .chat-history {
        border: 2px solid #ddd;
        padding: 10px;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .chat-entry {
        padding: 8px;
        margin-bottom: 10px;
        border-radius: 10px;
    }
    .chat-entry.user {
        background-color: rgba(0, 123, 255, 0.2);
    }
    .chat-entry.assistant {
        background-color: rgba(255, 193, 7, 0.2);
    }
    .reset-button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .reset-button:hover {
        background-color: #ff6161;
    }
    .center-image {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display image above the title and centralize it
st.markdown('<div class="center-image"><img src="https://www.stockvault.net/data/2016/12/25/219513/preview16.jpg" width="300"></div>', unsafe_allow_html=True)

# Display title with animation
st.markdown('<div class="main-title">World Travel Guide Chat: Journey with Gemini</div>', unsafe_allow_html=True)

# Display chat history in the main area
st.markdown('<div class="chat-history">', unsafe_allow_html=True)
for entry in st.session_state.chat_history:
    role = entry['role'].capitalize()
    content = entry['content']
    css_class = 'user' if entry['role'] == 'user' else 'assistant'
    st.markdown(f'<div class="chat-entry {css_class}"><strong>{role}:</strong> {content}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input box for user's question
user_input = st.text_input("What's your travel query?", key="input", placeholder="Type your message here...")

if user_input:
    # Add user's question to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get response from genai
    assistant_response = process_text(user_input)

    # Display the assistant's response
    st.markdown(f'<div class="chat-entry assistant"><strong>Assistant:</strong> {assistant_response}</div>', unsafe_allow_html=True)

    # Add the assistant's response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Clear the input box after submission
    st.experimental_rerun()

# Button to reset chat history
if st.button("Reset Chat", key="reset", help="Click to start a new journey"):
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    st.experimental_rerun()
