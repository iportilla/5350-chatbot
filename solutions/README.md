# Solutions (instructors)

> ⚠️ This repository is **public**, so students can see this folder. If you grade the coding tasks, consider moving `solutions/` to a private repo or branch before the term starts (see the [Instructor Guide](../guides/INSTRUCTOR_GUIDE.md#solutions-and-academic-integrity)).

| Lab | File | Notes |
|---|---|---|
| 2 | [`lab-02-memory/trim_history.py`](lab-02-memory/trim_history.py) | Sliding window + a summarization stretch version |
| 3 | *(prompt engineering)* | A sample hardened system prompt is in the Instructor Guide |
| 4A | [`lab-04-pizza-bot/app_pizza_bot_fsm.py`](lab-04-pizza-bot/app_pizza_bot_fsm.py) | Full rules-based FSM with confirmation and an HTML receipt |
| 4B | [`lab-04-pizza-bot/app_pizza_bot_llm.py`](lab-04-pizza-bot/app_pizza_bot_llm.py) | Hybrid: LLM JSON extraction, validation, regex fallback, deterministic policy |
| 5 | [`lab-05-reasoning-agent/tools.py`](lab-05-reasoning-agent/tools.py) | add / subtract / divide with a table-driven registry; errors returned as observations |

Run a solution from its folder, e.g.:
```bash
cd solutions/lab-04-pizza-bot && streamlit run app_pizza_bot_llm.py
```
