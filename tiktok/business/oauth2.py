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
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

DEFAULT_ACCESS_TOKEN_PATH = os.path.join(os.path.expanduser("~"), os.path.join(".tiktok", "access_token.json"))
OAUTH2_ACCESS_TOKEN_URL = "https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/"


class OAuth2:
    @staticmethod
    def _create_folders(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    @staticmethod
    def _write_access_token_to_file(access_token, advertiser_id, file_path):
        data = {"access_token": access_token, "advertiser_id": advertiser_id}
        with open(file_path, "w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def _write_to_file(response, file_path):
        dirname, filename_w_ext = os.path.split(file_path)
        if dirname:
            OAuth2._create_folders(dirname)
        filename = filename_w_ext.rsplit(".", 1)[0]
        access_token = response["data"]["access_token"]
        advertiser_ids = response["data"]["advertiser_ids"]
        for each in advertiser_ids:
            file_path = os.path.join(dirname, f"{filename}_{each}.json")
            OAuth2._write_access_token_to_file(access_token, each, file_path)
            logger.info(f"Token written to file: {file_path}")

    @staticmethod
    def get_access_token(app_id, secret, auth_code, write_to_file=True, file_path=DEFAULT_ACCESS_TOKEN_PATH):
        headers = {"Content-Type": "application/json"}
        params = {"app_id": app_id, "secret": secret, "auth_code": auth_code}
        response = requests.post(OAUTH2_ACCESS_TOKEN_URL, headers=headers, json=params)
        if response.ok:
            if write_to_file:
                OAuth2._write_to_file(response.json(), file_path)
            return response.json()
        return response.content
