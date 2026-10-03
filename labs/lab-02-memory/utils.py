# utils.py — Lab 2 helpers: the "logic" layer, kept separate from the Streamlit UI.
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = "You are a helpful AI chatbot that answers questions asked by the user."


def trim_history(messages, max_messages=10):
    """Return the part of the history we will actually send to the model.

    TODO (Lab 2, Task 4): implement a sliding window.
    Keep only the last `max_messages` messages so the prompt can't grow forever.
    Right now every message is sent, so cost grows with every turn.
    """
    return messages


def get_answer(messages):
    """Send the conversation to the model and return (reply_text, usage).

    The model is stateless: it only "remembers" what is inside `messages`.
    The system prompt is added on every call so the persona never gets lost.
    """
    payload = [{"role": "system", "content": SYSTEM_PROMPT}] + trim_history(messages)
    response = client.chat.completions.create(model=MODEL, messages=payload)
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "messages_sent": len(payload),
    }
    return response.choices[0].message.content, usage
