from openai import OpenAI
import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# Streamlit UI setup
st.title("💬 Chat with our MentalHealth-AI Tweet Assistant")
st.caption("🚀 A chatbot powered by OpenAI")

# Initialize conversation history in session state with a refined system message
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are a chatbot specialized in generating tweets focused on mental health. Your primary role is to create fun, "
                "engaging, and educational tweets that provide mental health insights suitable for a general audience, ideally people "
                "between the ages of 18 and 42. The tweets should be lighthearted yet informative, helping users understand mental health "
                "concepts in an accessible way. Stick to crafting tweets that are positive, supportive, and non-technical."
            )
        },
        {"role": "assistant", "content": "How can I help you craft a mental health tweet today?"}
    ]

# Display the conversation history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input field
if prompt := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get response from OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state["messages"]
        )
        msg = response.choices[0].message.content.strip()
        st.session_state["messages"].append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"An error occurred: {e}")
