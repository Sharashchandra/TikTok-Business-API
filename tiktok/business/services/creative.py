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
    HTTPMethods,
    AssetTypes
)

_logger = logging.getLogger(__name__)

class Creative:
    def __init__(self, client):
        self.client = client
        self.asset_type = None
    
    def __calculate_file_md5(self, file_path):
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    
    def __calculate_chunk_md5(self, chunk):
        return hashlib.md5(chunk).hexdigest()
    
    def __get_file_size(self, file_path):
        return os.path.getsize(file_path)
    
    @property
    def image(self):
        self.asset_type = AssetTypes.IMAGE.value
        return self
    
    @property
    def video(self):
        self.asset_type = AssetTypes.VIDEO.value
        return self
    
    @property
    def music(self):
        self.asset_type = AssetTypes.MUSIC.value
        return self
    
    def upload_file(self, file_path, file_name=None):
        file_size = self.__get_file_size(file_path)
        if file_size > (20 * 1024 * 1024):
            return self._upload_file_in_chunks(file_path, file_name)

        url = self.client.build_url(self.client.base_url, f"file/{self.asset_type}/ad/upload/")
        params = {
            "upload_type": "UPLOAD_BY_FILE",
            "file_name": file_name if file_name else os.path.basename(file_path),
            f"{self.asset_type}_signature": self.__calculate_file_md5(file_path),
        }
        files = {f"{self.asset_type}_file": open(file_path, "rb")}
        return self.client.make_request(HTTPMethods.POST.value, url, params, files=files)
    
    def upload_file_by_url(self, url, file_name=None):
        url = self.client.build_url(self.client.base_url, f"file/{self.asset_type}/ad/upload/")
        params = {
            "upload_type": "UPLOAD_BY_URL",
            f"{self.asset_type}_url": url,
        }
        params.update({"file_name": file_name}) if file_name else None
        return self.client.make_request(HTTPMethods.POST.value, url, params)
    
    def upload_file_by_file_id(self, file_id, file_name=None):
        url = self.client.build_url(self.client.base_url, f"file/{self.asset_type}/ad/upload/")
        params = {
            "upload_type": "UPLOAD_BY_FILE_ID",
            "file_id": file_id,
        }
        return self.client.make_request(HTTPMethods.POST.value, url, params)

    def _upload_file_in_chunks(self, file_path, file_name=None):
        upload_id, end_offset = self._start_chunk_upload(file_path, file_name)
        self._transfer_chunk(upload_id, end_offset, file_path)
        file_id = self._end_chunk_upload(upload_id)
        return self.upload_file_by_file_id(file_id)
    
    def _start_chunk_upload(self, file_path, file_name):
        url = self.client.build_url(self.client.base_url, "file/start/upload/")
        params = {
            "size": self.__get_file_size(file_path),
            "content_type": self.asset_type,
        }
        params.update({"file_name": file_name}) if file_name else None
        response = self.client.make_chunked_request(url, params)
        return (response["data"]["upload_id"], response["data"]["end_offset"])
    
    def _transfer_chunk(self, upload_id, end_offset, file_path, file_name=None):
        url = self.client.build_url(self.client.base_url, "file/transfer/upload/")
        start_offset = 0
        end_offset = end_offset
        chunk_size = (20*1024*1024)

        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                params = {
                    "upload_id": upload_id,
                    "start_offset": start_offset,
                    "signature": self.__calculate_chunk_md5(chunk),
                }
                files = {"file": chunk}
                response = self.client.make_chunked_request(url, params, files=files)
                start_offset = end_offset
                end_offset += chunk_size

    
    def _end_chunk_upload(self, upload_id):
        url = self.client.build_url(self.client.base_url, f"file/finish/upload/")
        response = self.client.make_chunked_request(url, {"upload_id": upload_id})
        return response["data"]['file_id']
    