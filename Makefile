init:
	pip install -r requirements.txt

test:
	python -m unittest discover -v -s tests

.PHONY: init test