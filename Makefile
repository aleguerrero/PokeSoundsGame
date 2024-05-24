install:
	python3 -m venv .venv
	pip install -r requirements.txt

run:
	python3 app.py