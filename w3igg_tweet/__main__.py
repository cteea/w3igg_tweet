"""A simple CLI tool to auto-generate Tweets for @web3isgreat."""

import argparse
import sys

from dotenv import load_dotenv

from .core import get_entry, tweet, get_driver


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="A CLI tool to auto-generate Tweets for @web3isgreat."
    )
    parser.add_argument(
        "-s",
        "--skip-check",
        action="store_true",
        help="tweet immediately without asking for confirmation",
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL of the entry to tweet (default is the latest entry)",
    )
    args = parser.parse_args()
    driver = get_driver()
    entry = get_entry(driver, args.url)
    if not args.skip_check:
        print("\nTitle")
        print("=====")
        print(entry["title"])
        print("\nDate")
        print("====")
        print(entry["date"])
        print("\nLink")
        print("====")
        print(entry["url"])
        print("\nScreenshot")
        print("==========")
        print(entry["screenshot"])
        print("\nAlt text")
        print("==========")
        print(entry["body-text"])
        confirmation = input("\nTweet it? [y/N]: ")
        if confirmation.lower() != "y":
            driver.quit()
            sys.exit()
    try:
        tweet(entry)
        title = entry["title"]
        print(f"Tweeted '{title}'.")
    except KeyError:
        print(
            "Error: Missing environment variables. Set the Twitter API access keys in .env.",
            file=sys.stderr,
        )
    finally:
        driver.quit()
