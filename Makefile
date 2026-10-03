# Shortcuts for macOS/Linux (and Windows with make installed).
# Windows without make: use scripts\run.cmd <target>, or the docker compose
# commands shown in guides/STUDENT_GUIDE.md.
#
#   make help          list everything
#   make setup         one-time local setup
#   make lab2          run a lab locally
#   make docker-lab2   run a lab in Docker (no Python install needed)

LABS := lab1 lab1-web lab2 lab3 lab4 lab4b lab5 lab6 solution4b

ifeq ($(OS),Windows_NT)
  VENV_PY := .venv\Scripts\python.exe
else
  VENV_PY := .venv/bin/python
endif

PORT ?= 8501
export PORT
COMPOSE := docker compose run --rm --service-ports labs
COMPOSE_NOPORTS := docker compose run --rm labs

.DEFAULT_GOAL := help
.PHONY: help setup check ping test clean $(LABS) \
        docker-build docker-check docker-test docker-shell $(addprefix docker-,$(LABS))

help: ## Show this help
	@echo "Local (needs Python 3.10+):"
	@echo "  make setup        Create .venv, install packages, create .env"
	@echo "  make check        Check Python, packages and API key"
	@echo "  make ping         ...and make one tiny real API call"
	@echo "  make lab1         Lab 1 terminal chatbot      make lab1-web   Lab 1 web chatbot"
	@echo "  make lab2         Lab 2 memory bot            make lab3       Lab 3 BloomBot"
	@echo "  make lab4         Lab 4A rules PizzaBot       make lab4b      Lab 4B hybrid PizzaBot"
	@echo "  make lab5         Lab 5 reasoning agent       make lab6       Lab 6 voice bot"
	@echo "  make test         Run Lab 5 tests (no API key needed)"
	@echo "  make clean        Delete caches and temp audio"
	@echo ""
	@echo "Docker (needs only Docker Desktop):"
	@echo "  make docker-build   Build the image (first time, ~2 min)"
	@echo "  make docker-check   Check setup inside Docker"
	@echo "  make docker-lab2    Run any lab in Docker: docker-lab1 ... docker-lab6"
	@echo "  make docker-test    Run Lab 5 tests in Docker"
	@echo "  make docker-shell   Open a terminal inside the container"
	@echo ""
	@echo "Port 8501 busy? Add PORT=8502, e.g.  make docker-lab2 PORT=8502  (then open localhost:8502)"

setup: ## One-time local setup
	bash scripts/setup.sh

$(VENV_PY):
	@echo "Course environment not found - running setup first."
	bash scripts/setup.sh

check: $(VENV_PY)
	$(VENV_PY) run.py check

ping: $(VENV_PY)
	$(VENV_PY) run.py check --ping

test: $(VENV_PY)
	$(VENV_PY) run.py test

$(LABS): $(VENV_PY)
	$(VENV_PY) run.py $@

clean:
	find . -name "__pycache__" -prune -exec rm -rf {} + ; \
	find . -name ".pytest_cache" -prune -exec rm -rf {} + ; \
	find . -name ".hypothesis" -prune -exec rm -rf {} + ; \
	find . -name "temp_audio*.mp3" -delete ; true

.env:
	cp .env.sample .env
	@echo ">> Created .env - open it in a text editor, paste your OPENAI_API_KEY, then run the command again."
	@exit 1

docker-build: .env
	docker compose build

docker-check: .env
	$(COMPOSE_NOPORTS) python run.py check

docker-test:
	$(COMPOSE_NOPORTS) python run.py test

docker-shell: .env
	$(COMPOSE_NOPORTS) bash

$(addprefix docker-,$(LABS)): .env
	$(COMPOSE) python run.py $(@:docker-%=%)
