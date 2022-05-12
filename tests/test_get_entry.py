import unittest
import w3igg_tweet
from selenium import webdriver

class TestGetEntry(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.driver = webdriver.Firefox()
    
    def tearDown(self):
        super().tearDown()
        self.driver.quit()

    def test_get_entry(self):
        """
        Test getting entry from W3IGG.
        """
        url = "https://web3isgoinggreat.com/?id=terra-luna-token-drops-in-price-by-98-amidst-ongoing-terrausd-stablecoin-collapse"

        result = w3igg_tweet.get_entry(self.driver, url)
        expected = {
            "date": "May 11, 2022",
            "title": "Terra $LUNA token drops in price by 98% amidst ongoing TerraUSD stablecoin collapse",
            "id": "terra-luna-token-drops-in-price-by-98-amidst-ongoing-terrausd-stablecoin-collapse",
            "screenshot": "tests/assets/tmp0rvw0hk2.png"
            }
        self.assertEqual(result["date"], expected["date"])
        self.assertEqual(result["title"], expected["title"])
        self.assertEqual(result["id"], expected["id"])
        with open(result["screenshot"], mode="rb") as f:
            result_screenshot = f.read()
        with open(expected["screenshot"], mode="rb") as f:
            expected_screenshot = f.read()
        self.assertEqual(result_screenshot, expected_screenshot)
    
if __name__ == "__main__":
    unittest.main()