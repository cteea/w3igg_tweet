"""
This module contains the core functionality for auto-generating tweets.

There are two core components:
- get_entry(driver, entry_url)
- tweet(entry)
"""

from urllib.parse import urlparse, parse_qs
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import tweepy
import html2text
from PIL import Image

W3IGG = "https://web3isgoinggreat.com/"

def get_driver():
    """
    Returns a Gecko WebDriver with options and preferences set.
    """
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    firefox_options.set_preference("layout.css.devPixelsPerPx", "4")
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager(log_level=0).install()),
        options=firefox_options
    )
    return driver

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
    """
    w3igg_url = W3IGG
    if entry_url is not None:
        w3igg_url = clean_and_normalize_url(entry_url)
    driver.set_window_size(650, 900)
    driver.get(w3igg_url)
    remove_fixed_at_bottom_buttons(driver)
    entry = get_top_most_entry(driver)
    body_text = get_entry_body_text(entry)
    screenshot_path = get_screenshot(entry)
    description = entry.find_element(by=By.CLASS_NAME, value="timeline-description")
    date = description.find_element(by=By.XPATH, value="//time").text
    title = description.find_element(by=By.XPATH, value="//h2/button/span").text
    title_button = description.find_element(by=By.XPATH, value="//h2/button")
    title_button.click()
    url = driver.current_url
    entry_id = get_id_from_url(url)
    driver.close()
    return {
        "date": date,
        "title": title,
        "body-text": body_text,
        "id": entry_id,
        "url": url,
        "screenshot": screenshot_path,
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
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', ' ')
    text = text.strip()
    text = text[:1000] # max Twitter AltText is 1000
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

def get_top_most_entry(driver):
    """
    Get the top most entry. For instance, if the `driver` is currently at
    https://web3isgoinggreat.com, then this will get the latest entry. If
    the `driver` is at a specific entry
    (e.g. https://web3isgoinggreat.com/?id=fbi-charges-eminifx-ceo-with-fraud)
    then it will get that entry.

    Parameters
    ----------
    driver : WebDriver
        A Selenium WebDriver

    Returns
    -------
    WebElement
        A Selenium WebElement of the latest entry
    """
    timeline = driver.find_element(by=By.ID, value="timeline")
    entries = timeline.find_elements(by=By.CLASS_NAME, value="timeline-entry")
    topmost = entries[0]
    return topmost


def get_screenshot(entry):
    """
    Take the screenshot of the entry.

    Parameters
    ----------
    entry : Selenium Remote WebDriver WebElement

    Returns
    -------
    str
        Path to the screenshot
    """
    screenshot_path = "./screenshot.png"
    entry.screenshot(screenshot_path)
    process_screenshot(screenshot_path)
    return screenshot_path

def remove_fixed_at_bottom_buttons(driver):
    """
    Remove the "Scroll to top" , "Show setting panel" buttons and the grift counter.

    Parameters
    ----------
    driver : WebDriver
    """
    driver.execute_script("""
    var buttons = document.getElementsByClassName("fix-at-bottom")[0];
    buttons.parentNode.removeChild(buttons);
    """)

def process_screenshot(screenshot_path):
    """
    Remove unwated portions of the screenshot and
    composite it onto a background at the center.

    Parameters
    ----------
    screenshot_path : str
        path to the screenshot
    """
    screenshot = Image.open(screenshot_path)
    width, height = screenshot.size
    margin = 50
    bg_w, bg_h = width+(margin*2), height+(margin*2)
    background = Image.new("RGB", (bg_w, bg_h), (238, 238, 238))
    offset = ((bg_w-width)//2, (bg_h-height)//2)
    background.paste(screenshot, offset)
    background = background.crop((190, 0, background.width-30, background.height))
    background.save(screenshot_path)
