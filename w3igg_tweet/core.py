"""
This module contains the core functionality for auto-generating tweets.

There are two core components:
- get_entry(driver, entry_url)
- tweet(entry)
"""

import tempfile
from urllib.parse import urlparse, parse_qs
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import tweepy
import html2text

W3IGG = "https://web3isgoinggreat.com/"


def get_entry(driver, entry_url=None):
    """
    Gets the entry from W3IGG. When `entry_url` is specified, this function will
    get the entry that the URL points to, otherwise get the latest entry.

    Parameters
    ----------
    driver : WebDriver
        A selenium webdriver.
    entry_url : str, optional
        Direct link to the entry.

    Returns
    -------
    dictionary
        a dictionary containing the following keys:
        - 'date': date of the entry
        - 'title': title of the entry
        - 'body-text': clean text from the body of the entry
        - 'id': id of the entry
        - 'url': URL of the entry
        - 'screenshot': path to the saved temporary screenshot of the entry

    NOTE: The screenshot will be saved as a temporary file only.
    """
    w3igg_url = W3IGG
    if entry_url is not None:
        w3igg_url = clean_and_normalize_url(entry_url)
    driver.get(w3igg_url)
    timeline = driver.find_element(by=By.ID, value="timeline")
    entries = timeline.find_elements(by=By.CLASS_NAME, value="timeline-entry")
    latest = entries[0]
    body_text = get_entry_body_text(latest)
    description = latest.find_element(by=By.CLASS_NAME, value="timeline-description")
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_f:
        tmp_screenshot_path = tmp_f.name + ".png"
    description.screenshot(tmp_screenshot_path)
    date = description.find_element(by=By.XPATH, value="//time").text
    title = description.find_element(by=By.XPATH, value="//h2/button/span").text
    title_button = description.find_element(by=By.XPATH, value="//h2/button")
    title_button.click()
    url = driver.current_url
    entry_id = get_id_from_url(url)
    return {
        "date": date,
        "title": title,
        "body-text": body_text,
        "id": entry_id,
        "url": url,
        "screenshot": tmp_screenshot_path,
    }


def tweet(entry):
    """
    Tweet the entry.

    Parameters
    ----------
    entry : a_dict (dict of str: str)
        A dictionary containing information about the entry with the following keys:
        - 'date': date of the entry
        - 'title': title of the entry
        - 'body-text': text from the entry body to be used as alt text for image
        - 'id': id of the entry
        - 'url': url of the entry
        - 'screenshot': path to the screenshot of the entry
    """
    consumer_key = os.environ["CONSUMER_KEY"]
    consumer_secret = os.environ["CONSUMER_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
    auth = tweepy.OAuth1UserHandler(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    api = tweepy.API(auth)
    entry_title = entry["title"]
    entry_date = entry["date"]
    entry_url = entry["url"]
    status = f"{entry_title}\n\n{entry_date}\n{entry_url}"
    media = api.simple_upload(entry["screenshot"])
    api.create_media_metadata(media.media_id, entry["body-text"])
    api.update_status(
        status=status,
        media_ids=[
            media.media_id,
        ],
    )


def get_entry_body_text(entry: WebElement) -> str:
    """
    This is a helper function that turns the provided `entry` DOM element into clean text.

    Parameters
    ----------
    entry : Selenium Remote WebDriver WebElement

    Returns
    -------
    str
        clean text of the entry body
    """
    entry = entry.find_element(by=By.CLASS_NAME, value="timeline-body-text-wrapper")
    html = entry.get_attribute("outerHTML")
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_emphasis = True
    text_maker.ignore_images = True
    text_maker.ignore_tables = True
    text = text_maker.handle(html)
    return text


def get_id_from_url(url):
    """
    Extract the id of the entry from a URL.

    Parameters
    ----------
    url : str
        The URL of the entry.

    Returns
    -------
    str
        id of the entry
    """
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    return parsed_qs["id"][0]


def clean_and_normalize_url(entry_url):
    """
    Clean and normalizes the given `entry_url`.

    Parameters
    ----------
    entry_url : str
        The link to the entry

    Returns
    -------
    str
        Fixed, cleaned-up, and normalized version of the URL
    """
    parsed = urlparse(entry_url)
    expected_netloc = urlparse(W3IGG).netloc
    if parsed.netloc != expected_netloc:
        raise Exception("invalid entry url", entry_url)
    queries = parse_qs(parsed.query)
    entry_id = ""
    for query, value in queries.items():
        if "id" in query:
            entry_id = value[0]
    if entry_id == "":
        raise Exception("invalid entry url", entry_url)
    normalized = f"{W3IGG}?id={entry_id}"
    return normalized
