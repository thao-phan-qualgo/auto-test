.PHONY: help install test format lint clean allure-report setup

help:
	@echo "Available commands:"
	@echo "  make setup         - Set up virtual environment and install dependencies"
	@echo "  make install       - Install dependencies (requires venv)"
	@echo "  make test          - Run all tests"
	@echo "  make format        - Format code with black and isort"
	@echo "  make lint          - Run flake8 and mypy checks"
	@echo "  make clean         - Clean generated files"
	@echo "  make allure-report - Generate Allure report"

setup:
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv venv; \
	fi
	@echo "Activate virtual environment with: source venv/bin/activate"
	@echo "Then run: make install"

install:
	@if [ -d "venv" ]; then \
		venv/bin/pip install -r requirements.txt; \
	else \
		python3 -m pip install -r requirements.txt --user; \
	fi

test:
	@if [ -d "venv" ]; then \
		venv/bin/behave; \
	else \
		behave; \
	fi

format:
	black . --line-length=100
	isort . --profile black

lint:
	flake8 . --max-line-length=100
	mypy .

clean:
	rm -rf reports/
	rm -rf logs/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

allure-report:
	allure generate reports/allure-results -o reports/allure-report --clean
	@echo "Allure report generated at reports/allure-report/index.html"
