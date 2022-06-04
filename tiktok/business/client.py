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
"""A client for TikTok Buisness API"""
import sys
import os
sys.path.insert(0, os.getcwd())
import json
import logging.config
import requests

from .services.campaign import Campaign

_logger = logging.getLogger(__name__)

class TikTokBuisnessAPI:
    """TikTok Buisness client used to configure settings and fetch services."""

    _session = None
    BUISNESS_URL = "https://business-api.tiktok.com/open_api"
    SANDBOX_URL = "https://sandbox-ads.tiktok.com/open_api"
    VERSION = "v1.2"
    
    def __init__(self, access_token, advertiser_id, sandbox=False):
        self.__access_token = access_token
        self.advertiser_id = advertiser_id
        self.base_url = self.SANDBOX_URL if sandbox else self.BUISNESS_URL
        self.base_url = self.build_url(self.base_url, self.VERSION)
        self.modules = {}

        if not self._session:
            self._create_session()
    
    def _create_session(self):
        self._session = requests.Session()
        self.__set_headers()

    def __set_headers(self):
        headers = {"Content-Type": "application/json", "Access-Token": self.__access_token}
        self._session.headers.update(headers)
    
    @property
    def campaign(self):
        if not self.modules.get("campaign"):
            self.modules["campaign"] = Campaign(advertiser_id=self.advertiser_id, client=self)
        return self.modules["campaign"]
    
    def build_url(self, base_url, service_endpoint):
        base_url = (base_url + "/") if not base_url.endswith("/") else base_url
        service_endpoint = (service_endpoint + "/") if not service_endpoint.endswith("/") else service_endpoint        
        
        return base_url + service_endpoint

    def make_request(self, method, url, params={}):
        print(method, url, params)
        params.update({"advertiser_id": self.advertiser_id}) if "advertiser_id" not in params else None
        response = self._session.request(method, url, json=params)
        return json.loads(response.json()) if response.ok else response.text