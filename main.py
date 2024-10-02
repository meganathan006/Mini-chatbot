import os
import streamlit as st
from groq import Groq


# Set up the page configuration
st.set_page_config(
    page_title="MiniChatbot",
    page_icon="🤖",
    layout="wide"
)

# Set up the title and instructions
st.title("Chatbot Interface")
st.write("Ask your questions below:")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize session state for user input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Define a function to handle user input submission
def submit_input():
    user_input = st.session_state.user_input

    if user_input:
        with open("./API.txt", "r") as file:
          api_key = file.read().strip()

        client = Groq(
            api_key=api_key
)

        # Prepare messages for context
        messages = [
            {"role": "user", "content": chat['user']} if 'user' in chat else {"role": "bot", "content": chat['bot']}
            for chat in st.session_state.chat_history[-5:]  # Get the last 5 messages
        ]

        # Add current user input
        messages.append({
            "role": "user",
            "content": user_input,
        })

        # Get the response from the bot
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content

        # Update chat history
        st.session_state.chat_history.append({"user": user_input, "bot": response})

        # Keep only the last 5 interactions
        st.session_state.chat_history = st.session_state.chat_history[-5:]

        # Clear the input field
        st.session_state.user_input = ""

# Function to start a new chat
def new_chat():
    st.session_state.chat_history = []

# Layout for input and new chat button
st.sidebar.title("Chat Options")
if st.sidebar.button("New Chat", key="new_chat_button"):
    new_chat()

# Display chat history
chat_container = st.container()
with chat_container:
    for chat in st.session_state.chat_history:
        st.write(f"**User:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")

# Placeholder for the user input
input_placeholder = st.empty()

# Input area for user messages
with input_placeholder:
    user_input = st.text_input("You:", key="user_input", on_change=submit_input)

# Automatically scroll to the bottom
st.markdown("<style>div.block-container {padding-bottom: 100px;}</style>", unsafe_allow_html=True)
