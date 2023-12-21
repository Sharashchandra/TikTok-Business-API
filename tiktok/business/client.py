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
import json
import logging.config
import os
import pkgutil

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TikTokBusinessClient:
    """TikTok Buisness client used to configure settings and fetch services."""

    _session = None
    BUISNESS_URL = "https://business-api.tiktok.com/open_api"
    SANDBOX_URL = "https://sandbox-ads.tiktok.com/open_api"
    VERSION = "v1.3"
    DEFAULT_ACCESS_TOKEN_FILE_PATH = os.path.join(os.path.expanduser("~"), os.path.join(".tiktok", "access_token.json"))

    def __init__(self, access_token, advertiser_id, sandbox=False):
        self.__access_token = access_token
        self.advertiser_id = str(advertiser_id)
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

        return cls(access_token=access_token, advertiser_id=advertiser_id, sandbox=sandbox)

    @classmethod
    def from_dict(cls, data):
        return cls(data["access_token"], data["advertiser_id"], data.get("sandbox"))

    def _sanitize_params(self, params):
        def cast_to_dtype(dictionary):
            for key, value in dictionary.items():
                dictionary[key] = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            return dictionary

        return cast_to_dtype(params)

    def _create_session(self):
        self._session = requests.Session()
        self._session.hooks["response"].append(self.__request_response_hook)
        self.__set_headers({"Access-Token": self.__access_token})

    def __set_headers(self, values):
        self._session.headers.update(values)

    def __set_advertiser_id(self, values):
        payload = {"advertiser_id": self.advertiser_id}

        values.update(payload)
        return values

    def __request_response_hook(self, *args, **kwargs):
        self._session.headers.pop("Content-Type") if "Content-Type" in self._session.headers else None

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
                logger.debug(f"{modname} module loaded successfully")
        logger.debug("Finished loading modules")

    def build_url(self, base_url, service_endpoint):
        base_url = (base_url + "/") if not base_url.endswith("/") else base_url
        service_endpoint = service_endpoint[1:] if service_endpoint.startswith("/") else service_endpoint
        service_endpoint = (service_endpoint + "/") if not service_endpoint.endswith("/") else service_endpoint

        return base_url + service_endpoint

    def make_request(self, method, url, data={}, params={}, files={}):
        params.update({"advertiser_id": self.advertiser_id}) if "advertiser_id" not in params else None
        self.__set_headers({"Content-Type": "application/json"}) if not files else None
        params = self._sanitize_params(params)
        data = self._sanitize_params(data)
        logger.debug(f"Method: {method}, URL: {url}, Params: {params}, Data: {data}")
        response = self._session.request(method, url, data=json.dumps(data), params=params, files=files)
        if not response.ok:
            return {"code": response.status_code, "message": response.content}

        response = response.json()
        return response

    def get(self, url, params):
        self.__set_headers({"Content-Type": "application/json"})
        params = self.__set_advertiser_id(values=params)
        params = self._sanitize_params(params)
        logger.debug(f"GET {url}, {params}")
        response = self._session.get(url, params=params)
        if not response.ok:
            return {"code": response.status_code, "message": response.content}

        response = response.json()
        return response

    def post(self, url, data, files=None):
        if not files:
            headers = {"Content-Type": "application/json"}
            self.__set_headers(headers)
        data = self.__set_advertiser_id(values=data)
        logger.debug(f"POST {self._session.headers}, {url}, {data}, files: {files.keys() if files else files}")

        if files:
            response = self._session.post(url, data=data, files=files)
        else:
            response = self._session.post(url, json=data)
        if not response.ok:
            return {"code": response.status_code, "message": response.content}

        response = response.json()
        return response

    def make_paginated_request(self, url, params):
        if "page_size" not in params:
            params.update({"page_size": 1000})
        initial_response = self.get(url, params=params)
        if initial_response["code"] == 0:
            total_pages = initial_response["data"]["page_info"]["total_page"]
            if total_pages > 1:
                for i in range(2, total_pages + 1):
                    params["page"] = i
                    response = self.get(url, params=params)
                    if response["code"] != 0:
                        return response
                    initial_response["data"]["list"].extend(response["data"]["list"])
                    initial_response["request_id"] = response["request_id"]
            initial_response["data"].pop("page_info")
        return initial_response
