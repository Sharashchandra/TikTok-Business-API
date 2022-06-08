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
import os
import json
import logging.config
import requests
import pkgutil

_logger = logging.getLogger(__name__)

class TikTokBusinessClient:
    """TikTok Buisness client used to configure settings and fetch services."""

    _session = None
    BUISNESS_URL = "https://business-api.tiktok.com/open_api"
    SANDBOX_URL = "https://sandbox-ads.tiktok.com/open_api"
    VERSION = "v1.2"
    DEFAULT_ACCESS_TOKEN_FILE_PATH = os.path.join(os.path.expanduser("~"), os.path.join(".tiktok", "access_token.json"))
    
    def __init__(self, access_token, advertiser_id, sandbox=False):
        self.__access_token = access_token
        self.advertiser_id = advertiser_id
        self.base_url = self.SANDBOX_URL if sandbox else self.BUISNESS_URL
        self.base_url = self.build_url(self.base_url, self.VERSION)

        if not self._session:
            self._create_session()
        
        self.discover_services()
    
    @classmethod
    def from_json_file(cls, json_file_path=DEFAULT_ACCESS_TOKEN_FILE_PATH, advertiser_id=None, sandbox=False):
        if not os.path.exists(json_file_path):
            raise Exception(f"File not found at {json_file_path}")
        with open(json_file_path, "r") as f:
            data = json.loads(f.read())
        access_token = data["access_token"]
        advertiser_id = data.get("advertiser_id") if not advertiser_id else advertiser_id

        if not advertiser_id:
            raise Exception("Advertiser id missing")

        return cls(access_token, advertiser_id, sandbox)
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["access_token"], data["advertiser_id"], data.get("sandbox"))
    
    def _sanitize_params(self, params):
        def cast_to_dtype(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    cast_to_dtype(value)
                else:
                    if isinstance(value, list):
                        dictionary[key] = json.dumps(value)
                    else:
                        dictionary[key] = str(value)

        cast_to_dtype(params)       
        return params
    
    def _create_session(self):
        self._session = requests.Session()
        self.__set_headers({"Access-Token": self.__access_token})

    def __set_headers(self, values):
        self._session.headers.update(values)
    
    def __get_module_cls(self, module_name, module):
        module_name = module_name.title().replace("_", "")
        if hasattr(module, module_name):
            return getattr(module, module_name)

    def discover_services(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        services_path = os.path.join(cwd, "services")
        for importer, modname, ispkg in pkgutil.iter_modules([services_path]):
            module = importer.find_module(modname).load_module(modname)
            cls_instance = self.__get_module_cls(modname, module)
            if cls_instance:
                setattr(self, modname, cls_instance(client=self))
                _logger.debug(f"{modname} module loaded successfully")
        _logger.debug("Finished loading modules")
    
    def build_url(self, base_url, service_endpoint):
        base_url = (base_url + "/") if not base_url.endswith("/") else base_url
        service_endpoint = service_endpoint[1:] if service_endpoint.startswith("/") else service_endpoint
        service_endpoint = (service_endpoint + "/") if not service_endpoint.endswith("/") else service_endpoint        
        
        return base_url + service_endpoint

    def make_request(self, method, url, params={}, files=None):
        params.update({"advertiser_id": self.advertiser_id}) if "advertiser_id" not in params else None
        self.__set_headers({"Content-Type": "application/json"}) if not files else None
        params = self._sanitize_params(params)
        print(method, url, params)
        if files:
            response = self._session.request(method, url, params=params, files=files)
        else:
            response = self._session.request(method, url, params=params)
        return response.json() if response.ok else response.text
    
    def make_chunked_request(self, url, params={}, files=None):
        params.update({"advertiser_id": self.advertiser_id}) if "advertiser_id" not in params else None
        params = self._sanitize_params(params)
        print("POST", url, params)
        if files:
            response = self._session.post(url, params=params, files=files)
        else:
            response = self._session.post(url, params=params)
        return response.json() if response.ok else response.text