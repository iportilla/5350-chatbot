# Lab 2, Task 4 SOLUTION — drop these into labs/lab-02-memory/utils.py


def trim_history(messages, max_messages=10):
    """Sliding window: send only the most recent `max_messages` messages."""
    return messages[-max_messages:]


# Stretch: summarise old turns instead of dropping them.
def trim_history_with_summary(messages, max_messages=10, summarize=None):
    """Keep recent turns verbatim and compress everything older into one message.

    `summarize` is a function that takes a list of messages and returns a short string,
    e.g. one more LLM call: "Summarize this conversation in 3 bullet points."
    """
    if len(messages) <= max_messages or summarize is None:
        return messages[-max_messages:]
    old, recent = messages[:-max_messages], messages[-max_messages:]
    summary = {"role": "system", "content": "Summary of earlier conversation: " + summarize(old)}
    return [summary] + recent
