# app_pizza_bot_llm.py — Lab 4 Part B STARTER: hybrid PizzaBot
# Complete the three TODOs (B1, B2, B3). Everything else already works.
#
# The LLM *understands* (extracts slots as JSON from free text).
# The code *decides* (which slot is missing, what to ask next, when the order is done).
# If the LLM call fails, deterministic regex extraction takes over.
import json
import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
MODEL = "gpt-4o-mini"

MENU = json.loads((Path(__file__).parent / "menu.json").read_text())
PIZZA_NAMES = [p["name"] for p in MENU["pizzas"]]
SLOTS = ["type", "size", "crust", "pickup_delivery", "time"]
QUESTIONS = {
    "type": f"What pizza would you like? We have: {', '.join(PIZZA_NAMES)}.",
    "size": "What size? (Small / Medium / Large)",
    "crust": "Which crust? (Thin / Regular / Pan)",
    "pickup_delivery": "Pickup or delivery?",
    "time": "What time would you like it?",
}

# TODO B1: write the extraction prompt.
# Tell the model to return ONLY a JSON object with the keys in SLOTS,
# list the allowed values for each key (use PIZZA_NAMES for "type"),
# and say to use null when the customer didn't mention something.
EXTRACTION_PROMPT = """TODO"""


# ---------------- Slot extraction ----------------
def extract_slots_llm(text):
    """Ask the LLM to turn free text into structured slots (JSON mode)."""
    # TODO B2: call client.chat.completions.create with
    #   - model=MODEL and temperature=0 (why 0? write it in your reflection)
    #   - response_format={"type": "json_object"}
    #   - a system message (EXTRACTION_PROMPT) and a user message (text)
    # then json.loads(...) the reply content and return validate(data).
    raise NotImplementedError("TODO B2")


def extract_slots_regex(text):
    """Deterministic fallback: same idea as the Part A finite-state bot."""
    t = text.lower()
    found = {}
    for keyword, name in [("pepperoni", "Classic Pepperoni"), ("veggie", "Veggie Delight"),
                          ("vegetarian", "Veggie Delight"), ("spicy", "Spicy Diablo"),
                          ("diablo", "Spicy Diablo")]:
        if keyword in t:
            found["type"] = name
            break
    if m := re.search(r"\b(small|medium|large)\b", t):
        found["size"] = m.group(1)
    if m := re.search(r"\b(thin|regular|pan)\b", t):
        found["crust"] = m.group(1)
    if "pick up" in t or "pickup" in t:
        found["pickup_delivery"] = "pickup"
    elif "deliver" in t:
        found["pickup_delivery"] = "delivery"
    if m := re.search(r"\b(\d{1,2}(:\d{2})?\s*(am|pm))\b", t):
        found["time"] = m.group(1)
    return found


def validate(data):
    """Never trust model output blindly: keep only known keys with allowed values."""
    # TODO B3: return a new dict that keeps only slots from SLOTS whose value is
    # not None/"" and (for type, size, crust, pickup_delivery) is an allowed value.
    # Try it: what happens if the model returns {"type": "Hawaiian"}?
    return data


def extract_slots(text):
    if client:
        try:
            return extract_slots_llm(text), "LLM"
        except Exception as e:  # network error, bad JSON, rate limit...
            st.toast(f"LLM unavailable, using regex fallback ({type(e).__name__})")
    return extract_slots_regex(text), "regex"


# ---------------- Dialog policy (deterministic) ----------------
def next_reply(order):
    missing = [s for s in SLOTS if order[s] is None]
    if missing:
        return QUESTIONS[missing[0]]
    price = next(p["price"] for p in MENU["pizzas"] if p["name"] == order["type"])
    return (f"Here's your order: **{order['size']} {order['type']}**, {order['crust']} crust, "
            f"{order['pickup_delivery']} at {order['time']} — **${price}**. Type **confirm** to place it.")


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="PizzaBot (LLM hybrid)", page_icon="🍕")
st.title("🍕 PizzaBot — LLM + State Machine")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! What can I get you today? 🍕"}]
    st.session_state.order = {s: None for s in SLOTS}
    st.session_state.confirmed = False

with st.sidebar:
    st.subheader("🧾 Order state (the 'slots')")
    st.json(st.session_state.order)
    if st.button("🔄 New order"):
        del st.session_state["messages"]
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if text := st.chat_input("e.g. A large veggie on thin crust, delivered at 7pm"):
    st.session_state.messages.append({"role": "user", "content": text})
    order = st.session_state.order

    if st.session_state.confirmed:
        reply = "Your order is already placed! Click **New order** to start another. 🍕"
    elif all(order.values()) and "confirm" in text.lower():
        st.session_state.confirmed = True
        reply = "🎉 Order confirmed! Thanks for choosing PizzaBot."
    else:
        slots, source = extract_slots(text)
        for slot, value in slots.items():
            order[slot] = value  # later messages can correct earlier answers
        reply = next_reply(order)
        if slots:
            reply = f"_(understood via {source}: {', '.join(slots)})_\n\n" + reply

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
