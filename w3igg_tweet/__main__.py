import argparse
import sys
from selenium import webdriver
from .core import get_entry, tweet

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web3 is great! Just by the dip.")
    parser.add_argument("--url", type=str, help="URL of the entry to tweet")
    args = parser.parse_args()
    options = webdriver.firefox.options.Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    entry = get_entry(driver, args.url)
    try:
        tweet(entry)
        title = entry["title"]
        print(f"Tweeted '{title}'.")
    except KeyError:
        print(
            "Error: Required environment variables are missing. Make sure the following environment variables are set:",
            file=sys.stderr,
        )
        print("- CONSUMER_KEY : your Twitter consumer key", file=sys.stderr)
        print("- CONSUMER_SECRET : your Twitter consumer secret", file=sys.stderr)
        print("- ACCESS_TOKEN : your Twitter access token", file=sys.stderr)
        print(
            "- ACCESS_TOKEN_SECRET : your Twitter access token secret", file=sys.stderr
        )
    finally:
        driver.quit()
