"""Tests"""

import filecmp
import unittest

import w3igg_tweet


class TestGetEntry(unittest.TestCase):
    """Test getting entry."""

    def setUp(self) -> None:
        super().setUp()
        self.driver = w3igg_tweet.get_driver()

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
            "body-text": "Terraform Labs develops two cryptocurrencies: TerraUSD ($UST), an algorithmic stablecoin meant to be pegged to the U.S. dollar, and $LUNA, a crypto asset used both for speculation and to help maintain the UST peg. As UST dramatically lost its peg throughout early May, Luna plummeted in value alongside it. Luna was trading between $80 and $90 in the first days of May, but as of May 11 had lost 98% of its value and was hovering between $2 and $3. By midday on May 12, the token was trading at or below $0.01. Such a dramatic crash in a cryptocurrency that was in the top ten by market cap has been devastating to some. Some members of the Terra/Luna community on Reddit have spoken of being massively over-invested in Luna, with some describing losing their life savings and appearing to be in crisis.",
            "id": "terra-luna-token-drops-in-price-by-98-amidst-ongoing-terrausd-stablecoin-collapse",
            "url": url,
            "screenshot": "tests/assets/sample_screenshot.png",
        }
        self.assertEqual(result["date"], expected["date"])
        self.assertEqual(result["title"], expected["title"])
        self.assertEqual(result["body-text"], expected["body-text"])
        self.assertEqual(result["id"], expected["id"])
        self.assertEqual(result["url"], expected["url"])
        result_screenshot = result["screenshot"]
        expected_screenshot = expected["screenshot"]
        self.assertTrue(
            filecmp.cmp(result["screenshot"], expected["screenshot"]),
            f"Incorrect screenshot produced: expected {expected_screenshot}, but got {result_screenshot}",
        )


if __name__ == "__main__":
    unittest.main()
