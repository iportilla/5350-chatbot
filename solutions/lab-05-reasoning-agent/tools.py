"""
Lab 5 SOLUTION — tool registry extended with add, subtract and divide.

Copy over labs/lab-05-reasoning-agent/reasoning_agent/tools.py to try it.
A table-driven registry replaces the if/elif router so adding a tool is one entry.
"""


def multiply(a: float, b: float) -> float:
    return a * b


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


TOOLS = {
    "multiply": (multiply, "Multiply two numbers together"),
    "add": (add, "Add two numbers together"),
    "subtract": (subtract, "Subtract b from a"),
    "divide": (divide, "Divide a by b"),
}


def get_tool_definitions() -> list:
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                    "required": ["a", "b"],
                },
            },
        }
        for name, (_, description) in TOOLS.items()
    ]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")
    a, b = tool_input.get("a"), tool_input.get("b")
    if a is None or b is None:
        raise ValueError(f"{tool_name} requires 'a' and 'b' parameters")
    try:
        return str(TOOLS[tool_name][0](a, b))
    except ValueError as e:
        # Return the error to the model as an observation instead of crashing the loop
        return f"Error: {e}"
