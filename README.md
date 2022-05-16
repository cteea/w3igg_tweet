# Tweet Generator for @web3isgreat

Automatically tweet an entry from [Web3IsGoingGreat](https://web3isgoinggreat.com).

## Install
Clone the repo:
```
git clone https://github.com/0pling/w3igg_tweet.git
```

`cd` into the cloned repo and initialize:
```
make init
```

Put your Twitter API authentication credentials inside `.env`:
```
CONSUMER_KEY='consumer key'
CONSUMER_SECRET='consumer secret'
ACCESS_TOKEN='access token'
ACCESS_TOKEN_SECRET='access token secret'
``` 

## Usage
`cd` into "w3igg_tweet" and activate the Python virtual environment:
```
source ./venv/bin/activate
```

To tweet the latest entry from [Web3IsGoingGreat](https://web3isgoinggreat.com):
```
python -m w3igg_tweet
```

To tweet a particular entry from [Web3IsGoingGreat](https://web3isgoinggreat.com):
```
python -m w3igg_tweet --url https://web3isgoinggreat.com/?id=some-entry-id
```

To tweet without asking for confimation:
```
python -m w3igg_tweet --skip-check
```

To see all the available options:
```
python -m w3igg_tweet -h
```