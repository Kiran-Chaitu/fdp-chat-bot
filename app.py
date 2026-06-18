from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
client  = Groq(api_key=os.getenv("GROQ_API_KEY"))
st.header("Groq Bot")
st.sidebar("Settings")
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role" : "system",
        "content" : """you are a helpful assistant.
        Rules:
            1. Always provide a complete answer.
            2. Never stop in the middle of a sentence.
            3. If the response is long, summarize it.
            4. Prefer a short complete answer over a long incomplete answer.
            5. Maximum 3 sentences unless the user asks for detials.
        """
    }]

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("User").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("AI").write(msg["content"])

question  = st.chat_input("Ask a question: ")
if question:
    st.session_state.messages.append({"role":"user" , "content" : question})
    memory = st.session_state.messages[0:1] + st.session_state.messages[-6:]
    response  = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages =memory,max_tokens=100)
    answer  = response.choices[0].message.content
    st.session_state.messages.append({"role" : "assistant" , "content":answer})
    usage  = response.usage
    print(f"Total tokens used: {usage.total_tokens}")
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Completion tokens: {usage.completion_tokens}")
    st.rerun()
