verify: f
	mypy .
	pylint .

f:
	isort .
	black .

t:
	pytest tests/
