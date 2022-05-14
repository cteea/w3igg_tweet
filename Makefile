.SILENT: requirements .env init venv

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SOURCE_VENV = source $(VENV)/bin/activate

init: venv .env requirements
	echo "Initialization done."
	echo "Please put your Twitter API access keys inside the '.env' file."

requirements: venv
	echo "Installing requirements..."
	$(PIP) install -q -r requirements.txt

test: venv
	$(PYTHON) -m unittest discover -v -s tests

.env:
	echo "Creating .env file..."
	touch ./.env
	echo "CONSUMER_KEY='your Twitter consumer key'" >> .env
	echo "CONSUMER_SECRET='your Twitter consumer secret'" >> .env
	echo "ACCESS_TOKEN='your Twitter access token'" >> .env
	echo "ACCESS_TOKEN_SECRET='your Twitter access token secret'" >> .env

venv:
	echo "Creating Python virtual environment..."
	python3 -m venv ./venv
	$(PIP) install --upgrade pip

.PHONY: requirements test init