# MIT License

# Copyright (c) 2022 Sharashchandra

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import unittest

sys.path.append("../tiktok/")
from tiktok.business.client import TikTokBusinessClient


class client_TestCases(unittest.TestCase):
    def test_business_client(self):
        client = TikTokBusinessClient(access_token="ABC", advertiser_id="123")
        self.assertEqual(client.advertiser_id, "123")
        self.assertEqual(client.base_url, "https://business-api.tiktok.com/open_api/v1.2/")

    def test_sandbox_client(self):
        client = TikTokBusinessClient(access_token="ABC", advertiser_id="123", sandbox=True)
        self.assertEqual(client.advertiser_id, "123")
        self.assertEqual(client.base_url, "https://sandbox-ads.tiktok.com/open_api/v1.2/")

    def test_services_available(self):
        client = TikTokBusinessClient(access_token="ABC", advertiser_id="123")
        available_services = ["ad", "ad_group", "audience", "campaign", "creative", "reports"]
        for service in available_services:
            self.assertTrue(hasattr(client, service), True)

    def test_content_type_not_in_headers(self):
        client = TikTokBusinessClient(access_token="ABC", advertiser_id="123")
        r = client.get("https://run.mocky.io/v3/0f18b7f9-ef93-478b-84d2-7da783527e1a")
        headers = client._session.headers
        self.assertEqual(headers.get("Content-Type"), None)


if __name__ == "__main__":
    # Build the test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(client_TestCases))

    # Running tests
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(len(result.errors) + len(result.failures))
