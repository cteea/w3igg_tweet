import tempfile
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs

W3IGG = "https://web3isgoinggreat.com/"

def get_entry(driver, entry_url=""):
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
        - 'id': id of the entry
        - 'screenshot': path to the saved temporary screenshot of the entry

    NOTE: The screenshot will be saved as a temporary file only.
    """
    w3igg_url = W3IGG
    if len(entry_url) > 0:
        w3igg_url = entry_url
    driver.get(w3igg_url)
    timeline = driver.find_element(by=By.ID, value="timeline")
    entries = timeline.find_elements(by=By.CLASS_NAME, value="timeline-entry")
    latest = entries[0]
    description = latest.find_element(by=By.CLASS_NAME, value="timeline-description")
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp_f:
        tmp_screenshot_path = tmp_f.name
    description.screenshot(tmp_screenshot_path)
    date = description.find_element(by=By.XPATH, value="//time").text
    title = description.find_element(by=By.XPATH, value="//h2/button/span").text
    title_button = description.find_element(by=By.XPATH, value="//h2/button")
    title_button.click()
    id = get_id_from_url(driver.current_url)
    return {"date": date, "title": title, "id": id, "screenshot": tmp_screenshot_path}

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
    u = urlparse(url)
    q = parse_qs(u.query)
    return q["id"][0]
