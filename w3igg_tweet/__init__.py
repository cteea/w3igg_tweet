from selenium import webdriver
from .core import get_entry

def main():
    driver = webdriver.Firefox()
    latest = get_entry(driver)
    print(latest)
    driver.quit()

if __name__ == "__main__":
    main()