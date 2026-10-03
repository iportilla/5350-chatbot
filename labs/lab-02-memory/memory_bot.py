# memory_bot.py — Lab 2: Streamlit chatbot with conversation memory
import streamlit as st

from utils import get_answer

st.set_page_config(page_title="Memory Chatbot", page_icon="💬")
st.title("💬 Chatbot with Memory")

# --- Session state: survives Streamlit's top-to-bottom reruns ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How may I assist you today?"}
    ]
if "usage_log" not in st.session_state:
    st.session_state.usage_log = []  # one entry per turn, so we can watch cost grow

with st.sidebar:
    if st.button("🧹 Clear conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared. How can I help?"}
        ]
        st.session_state.usage_log = []
        st.rerun()

    st.subheader("📈 Prompt size per turn")
    if st.session_state.usage_log:
        st.line_chart([u["prompt_tokens"] for u in st.session_state.usage_log])
        last = st.session_state.usage_log[-1]
        st.caption(
            f"Last turn: {last['messages_sent']} messages sent, "
            f"{last['prompt_tokens']} prompt tokens, {last['completion_tokens']} completion tokens"
        )
    else:
        st.caption("Send a message to start tracking tokens.")

# --- Render history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- New turn ---
user_input = st.chat_input("Type your message…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply, usage = get_answer(st.session_state.messages)
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.usage_log.append(usage)
    st.rerun()  # refresh the sidebar chart
