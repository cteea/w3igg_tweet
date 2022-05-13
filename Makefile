init: .env
	pip install -r requirements.txt
	echo "Please put your Twitter API access keys inside the '.env' file."

test:
	python -m unittest discover -v -s tests

.env:
	touch ./.env
	echo "CONSUMER_KEY='your Twitter consumer key'" >> .env
	echo "CONSUMER_SECRET='your Twitter consumer secret'" >> .env
	echo "ACCESS_TOKEN='your Twitter access token'" >> .env
	echo "ACCESS_TOKEN_SECRET='your Twitter access token secret'" >> .env

.PHONY: init test