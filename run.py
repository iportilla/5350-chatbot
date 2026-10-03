"""Course launcher: works the same on Windows, macOS, Linux and inside Docker.

    python run.py                 # list everything you can run
    python run.py check           # check your setup (Python, packages, API key)
    python run.py check --ping    # ...and make one tiny real API call
    python run.py lab2            # start Lab 2
    python run.py test            # run Lab 5's tests (no API key needed)

You never need to `cd` into a lab folder or activate anything; this script does it.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# name: (folder, file, kind, description)
TARGETS = {
    "lab1":     ("labs/lab-01-first-api-call",       "cli_chat.py",             "python",    "Lab 1 - terminal chatbot"),
    "lab1-web": ("labs/lab-01-first-api-call",       "web_chat.py",             "streamlit", "Lab 1 - web chatbot (no memory)"),
    "lab2":     ("labs/lab-02-memory",               "memory_bot.py",           "streamlit", "Lab 2 - chatbot with memory"),
    "lab3":     ("labs/lab-03-persona-bot",          "bloom_bot.py",            "streamlit", "Lab 3 - BloomBot persona"),
    "lab4":     ("labs/lab-04-pizza-bot/starter",    "app_pizza_bot.py",        "streamlit", "Lab 4 Part A - rules-based PizzaBot"),
    "lab4b":    ("labs/lab-04-pizza-bot/starter",    "app_pizza_bot_llm.py",    "streamlit", "Lab 4 Part B - hybrid LLM PizzaBot"),
    "lab5":     ("labs/lab-05-reasoning-agent",      "app.py",                  "streamlit", "Lab 5 - reasoning agent"),
    "lab6":     ("labs/lab-06-voice-bot",            "app.py",                  "streamlit", "Lab 6 - voice bot (needs a mic)"),
    "test":     ("labs/lab-05-reasoning-agent",      "",                        "pytest",    "Lab 5 - run the tests"),
    "solution4b": ("solutions/lab-04-pizza-bot",     "app_pizza_bot_llm.py",    "streamlit", "Instructor - hybrid PizzaBot solution"),
}

REQUIRED_PACKAGES = ["openai", "streamlit", "dotenv", "pytest", "hypothesis"]


def ok(msg):
    print(f"  [ OK ] {msg}")


def bad(msg, fix):
    print(f"  [FAIL] {msg}\n         -> {fix}")


def check(ping=False):
    print("Checking your setup...\n")
    problems = 0

    if sys.version_info >= (3, 10):
        ok(f"Python {sys.version.split()[0]}")
    else:
        problems += 1
        bad(f"Python {sys.version.split()[0]} is too old", "Install Python 3.10 or newer (see guides/STUDENT_GUIDE.md)")

    in_venv = sys.prefix != sys.base_prefix or os.getenv("IN_DOCKER") == "1"
    if in_venv:
        ok("Running inside the course environment (.venv or Docker)")
    else:
        print("  [WARN] Not running inside .venv. Use the scripts/ launchers, or activate .venv first")

    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            ok(f"package '{pkg}' installed")
        except ImportError:
            problems += 1
            bad(f"package '{pkg}' missing", "Run the setup script again (scripts/setup.sh or scripts\\setup.cmd)")

    env_file = ROOT / ".env"
    key = None
    if env_file.exists():
        ok(".env file found")
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            pass
    elif os.getenv("OPENAI_API_KEY"):
        ok("OPENAI_API_KEY set in the environment")
    else:
        problems += 1
        bad(".env file not found in the repo folder", "Copy .env.sample to .env and paste your key into it")

    key = os.getenv("OPENAI_API_KEY", "").strip().strip('"')
    if not key or key in ("sk-...", "sk-###"):
        problems += 1
        bad("OPENAI_API_KEY is empty or still the placeholder", "Open .env in a text editor and paste your real key after OPENAI_API_KEY=")
    elif not key.startswith("sk-"):
        problems += 1
        bad("OPENAI_API_KEY doesn't look like an OpenAI key (should start with 'sk-')", "Re-copy the key from platform.openai.com/api-keys")
    else:
        ok(f"OPENAI_API_KEY looks valid (sk-...{key[-4:]})")

    if ping and key:
        try:
            from openai import OpenAI
            reply = OpenAI(api_key=key).chat.completions.create(
                model="gpt-4o-mini", max_tokens=5,
                messages=[{"role": "user", "content": "Say OK"}],
            ).choices[0].message.content
            ok(f"API call worked (model replied: {reply!r})")
        except Exception as e:
            problems += 1
            bad(f"API call failed: {type(e).__name__}: {str(e)[:150]}", "See the troubleshooting table in guides/STUDENT_GUIDE.md")

    print()
    if problems:
        print(f"{problems} problem(s) found. Fix the [FAIL] lines above and run the check again.")
        return 1
    print("All good! You are ready for Lab 1.")
    return 0


def usage():
    print(__doc__)
    print("Targets:")
    for name, (_, _, _, desc) in TARGETS.items():
        print(f"  {name:<11} {desc}")
    print(f"  {'check':<11} Check your setup (add --ping for a real API call)")


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help", "list"):
        usage()
        return 0
    name = argv[0].lower()
    if name == "check":
        return check(ping="--ping" in argv)
    if name not in TARGETS:
        print(f"Unknown target '{name}'.\n")
        usage()
        return 2

    folder, file, kind, desc = TARGETS[name]
    cwd = ROOT / folder
    if kind == "python":
        cmd = [sys.executable, file]
    elif kind == "streamlit":
        cmd = [sys.executable, "-m", "streamlit", "run", file]
        port = os.getenv("PORT", "8501") if os.getenv("IN_DOCKER") else "8501"
        print(f"Starting {desc}...\nOpen http://localhost:{port} in your browser. Press Ctrl+C here to stop.\n")
    else:  # pytest
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
    try:
        return subprocess.call(cmd + argv[1:], cwd=cwd)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
