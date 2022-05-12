import filecmp
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
            "body-text": 'Terraform Labs develops two cryptocurrencies: TerraUSD ($UST), an algorithmic\nstablecoin meant to be pegged to the U.S. dollar, and $LUNA, a crypto asset\nused both for speculation and to help maintain the UST peg. As UST\ndramatically lost its peg throughout early May, Luna plummeted in value\nalongside it. Luna was trading between $80 and $90 in the first days of May,\nbut as of May 11 had lost 98% of its value and was hovering between $2 and $3.\nBy midday on May 12, the token was trading at or below $0.01.\n\nSuch a dramatic crash in a cryptocurrency that was in the top ten by market\ncap has been devastating to some. Some members of the Terra/Luna community on\nReddit have spoken of being massively over-invested in Luna, with some\ndescribing losing their life savings and appearing to be in crisis.\n\n',
            "id": "terra-luna-token-drops-in-price-by-98-amidst-ongoing-terrausd-stablecoin-collapse",
            "url": url,
            "screenshot": "tests/assets/sample_screenshot.png"
            }
        self.assertEqual(result["date"], expected["date"])
        self.assertEqual(result["title"], expected["title"])
        self.assertEqual(result["body-text"], expected["body-text"])
        self.assertEqual(result["id"], expected["id"])
        self.assertEqual(result["url"], expected["url"])
        self.assertTrue(filecmp.cmp(result["screenshot"], expected["screenshot"]),
                        "Incorrect screenshot produced: expected {}, but got {}".format(
                            expected["screenshot"],
                            result["screenshot"]
                            ))
    
if __name__ == "__main__":
    unittest.main()