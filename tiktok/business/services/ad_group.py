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
from .constants import (
    ServiceStatus,
    HTTPMethods
)

_logger = logging.getLogger(__name__)

class AdGroup:
    def __init__(self, client):
        self.client = client
        self.ad_group_base_url = self.client.build_url(self.client.base_url, "adgroup/")
    
    def get_ad_group(self, params):
        url = self.client.build_url(self.ad_group_base_url, "get/")
        return self.client.make_request(HTTPMethods.POST.value, url, params or {})
    
    def create_ad_group(self, params):
        url = self.client.build_url(self.ad_group_base_url, "create/")
        return self.client.make_request(HTTPMethods.POST.value, url, params or {})
    
    def update_ad_group(self, params):
        url = self.client.build_url(self.ad_group_base_url, "update/")
        return self.client.make_request(HTTPMethods.POST.value, url, params or {})
    
    def update_ad_group_budget(self, params):
        url = self.client.build_url(self.ad_group_base_url, "update/budget/")
        return self.client.make_request(HTTPMethods.POST.value, url, params or {})
    
    def _update_ad_group_status(self, adgroup_ids, status):
        adgroup_ids = [adgroup_ids] if isinstance(adgroup_ids, str) else adgroup_ids
        params = {"adgroup_ids": adgroup_ids, "opt_status": status}
        url = self.client.build_url(self.ad_group_base_url, "update/status/")
        return self.client.make_request(HTTPMethods.POST.value, url, params or {})
    
    def enable_ad_group(self, adgroup_ids):
        return self._update_ad_group_status(adgroup_ids=adgroup_ids, status=ServiceStatus.ENABLE.value)
    
    def disable_ad_group(self, adgroup_ids):
        return self._update_ad_group_status(adgroup_ids=adgroup_ids, status=ServiceStatus.DISABLE.value)
    
    def delete_ad_group(self, adgroup_ids):
        return self._update_ad_group_status(adgroup_ids=adgroup_ids, status=ServiceStatus.DELETE.value)