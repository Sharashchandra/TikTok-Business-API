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
from http import HTTPMethod


class Advertiser:
    def __init__(self, client):
        self.client = client
        self.advertiser_base_url = self.client.build_url(self.client.base_url, "advertiser/")

    def get_advertiser_info(self, advertiser_ids, params=None):
        if not params:
            params = {}
        params["advertiser_ids"]: advertiser_ids
        url = self.client.build_url(self.advertiser_base_url, "info/")
        return self.client.get(HTTPMethod.GET, url, params)

    def get_current_advertiser_info(self, params=None):
        return self.get_advertiser_info(advertiser_ids=[self.client.advertiser_id], params=params or {})
