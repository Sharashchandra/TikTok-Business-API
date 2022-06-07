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
import hashlib

from PIL import Image

from .constants import (
    ServiceStatus,
    HTTPMethods
)

_logger = logging.getLogger(__name__)

class Creative:
    def __init__(self, client):
        self.client = client
    
    def __calculate_asset_md5(self, asset_file_path):
        md5hash = hashlib.md5(Image.open(asset_file_path).tobytes())
        return md5hash.hexdigest()
    
    def upload_image_by_file(self, image_file_path, file_name=None):
        raise NotImplementedError
    
    def upload_image_by_url(self, params={}):
        url = self.client.build_url(self.client.base_url, "/file/image/ad/upload/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def upload_image_by_file_id(self, params={}):
        url = self.client.build_url(self.client.base_url, "/file/image/ad/upload/")
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    