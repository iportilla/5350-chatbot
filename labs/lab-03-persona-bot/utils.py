# utils.py — Lab 3 helper: call the LLM with whatever system prompt the app provides.
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.7  # Task 3: try 0.0 and 1.2 and compare the bouquets you get


def get_answer(messages):
    """Return the assistant's reply. `messages` must already start with a system prompt."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content
