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
import logging
import requests
import csv

from tiktok.business.services.constants import (
    HTTPMethods,
)

_logger = logging.getLogger(__name__)

class Reports:
    def __init__(self, client):
        self.client = client
        self.reports_base_url = self.client.build_url(self.client.base_url, "reports/")
    
    def get_synchronous_report(self, params={}):
        url = self.client.build_url(self.reports_base_url, "integrated/get/")
        return self.client.make_request(HTTPMethods.GET.value, url, params)
    
    def create_asynchronous_report_task(self, params={}):
        url = self.client.build_url(self.reports_base_url, "integrated/get/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def check_asynchronous_report_task(self, params={}):
        url = self.client.build_url(self.reports_base_url, "task/check/")
        return self.client.make_request(HTTPMethods.GET.value, url, params)
    
    def __create_files(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    
    def __stream_csv_to_file(self, url, task_id, file_path):
        params = {"advertiser_id": self.client.advertiser_id, "task_id": task_id}
        with open(file_path, "w") as f, self.client._session.get(url, params=params, stream=True) as r:
            for line in r.iter_lines():
                f.write(line + "\n".encode("utf-8"))
        return file_path
    
    def download_asynchronous_report(self, task_id, file_path):
        url = self.client.build_url(self.reports_base_url, "task/download/")
        self.__create_files(file_path)
        return self.__stream_csv_to_file(url, task_id, file_path)