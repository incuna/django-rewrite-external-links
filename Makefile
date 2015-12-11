test:
	@coverage run ./tests/run.py
	@coverage report --show-missing
	@flake8
