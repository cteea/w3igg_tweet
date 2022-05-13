.SILENT: requirements .env init

init: .env requirements
	echo "Initialization done."
	echo "Please put your Twitter API access keys inside the '.env' file."

requirements:
	echo "Installing requirements..."
	pip install -q -r requirements.txt

test:
	python -m unittest discover -v -s tests

.env:
	echo "Creating .env file..."
	touch ./.env
	echo "CONSUMER_KEY='your Twitter consumer key'" >> .env
	echo "CONSUMER_SECRET='your Twitter consumer secret'" >> .env
	echo "ACCESS_TOKEN='your Twitter access token'" >> .env
	echo "ACCESS_TOKEN_SECRET='your Twitter access token secret'" >> .env

.PHONY: requirements test init