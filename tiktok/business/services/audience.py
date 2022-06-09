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
import os
import logging
import hashlib
from tiktok.business.services.constants import (
    ServiceStatus,
    HTTPMethods
)

_logger = logging.getLogger(__name__)

class Audience:
    def __init__(self, client):
        self.client = client
        self.audience_base_url = self.client.build_url(self.client.base_url, "dmp/custom_audience/")
    
    def __calculate_file_md5(self, file_path):
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    
    def get_all_audiences(self, params={}):
        url = self.client.build_url(self.audience_base_url, "list/")
        return self.client.make_paginated_request(HTTPMethods.GET.value, url, params)
    
    def get_audience_details(self, params={}):
        url = self.client.build_url(self.audience_base_url, "get/")
        return self.client.make_request(HTTPMethods.GET.value, url, params)
    
    def upload_audience(self, file_path, calculate_type):
        if os.path.getsize(file_path) > (50 * 1024 * 1024):
            raise Exception("File size should be less than 50MB")
        url = self.client.build_url(self.audience_base_url, "file/upload/")
        params = {
            "calculate_type": calculate_type,
            "file_signature": self.__calculate_file_md5(file_path)
        }
        files = {"file": open(file_path, "rb")}
        return self.client.make_request(HTTPMethods.POST.value, url, params, files=files)
    
    def create_audience_by_file(self, params={}):
        url = self.client.build_url(self.audience_base_url, "create/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def create_audience_by_rule(self, params={}):
        url = self.client.build_url(self.audience_base_url, "rule/create/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def create_lookalike_audience(self, params={}):
        url = self.client.build_url(self.audience_base_url, "lookalike/create/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def update_audience(self, params={}):
        url = self.client.build_url(self.audience_base_url, "update/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def delete_audience(self, params={}):
        url = self.client.build_url(self.audience_base_url, "delete/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def share_audience(self, params={}):
        url = self.client.build_url(self.audience_base_url, "share/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def cancel_audience_sharing(self, params={}):
        url = self.client.build_url(self.audience_base_url, "share/cancel/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def get_audience_sharing_log(self, params={}):
        url = self.client.build_url(self.audience_base_url, "share/log/")
        return self.client.make_request(HTTPMethods.GET.value, url, params)