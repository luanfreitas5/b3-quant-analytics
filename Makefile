.PHONY: install format test run

install:
	pip install -r requirements.txt

format:
	black src tests scripts

test:
	pytest

run:
	python src/main.py run
