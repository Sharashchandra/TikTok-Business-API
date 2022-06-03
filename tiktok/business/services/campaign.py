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
    Urls,
    ServiceStatus,
    HTTPMethods
)

_logger = logging.getLogger(__name__)

class Campaign:
    def __init__(self, client):
        self.client = client
    
    def get_campaign(self, params):
        _logger.debug(f"Campaign GET: {params}")
        return self.client.make_request(HTTPMethods.GET.value, Urls.CAMPAIGN_GET_URL.value, params)
    
    def create_campaign(self, params):
        return self.client.make_request(HTTPMethods.POST.value, Urls.CAMPAIGN_CREATE_URL, params)
    
    def update_campaign(self, params):
        return self.client.make_request(HTTPMethods.POST.value, Urls.CAMPAIGN_UPDATE_URL, params)
    
    def _update_campaign_status(self, campaign_ids, status):
        campaign_ids = list(campaign_ids) if isinstance(campaign_ids, str) else campaign_ids
        params = {"campaign_ids": campaign_ids, "opt_status": status}
        return self.client.make_request(HTTPMethods.POST.value, Urls.CAMPAIGN_UPDATE_STATUS_URL.value, params)
    
    def enable_campaign(self, campaign_ids):
        return self._update_campaign_status(campaign_ids=campaign_ids, status=ServiceStatus.ENABLE.value)
    
    def disable_campaign(self, campaign_ids):
        return self._update_campaign_status(campaign_ids=campaign_ids, status=ServiceStatus.DISABLE.value)
    
    def delete_campaign(self, campaign_ids):
        return self._update_campaign_status(campaign_ids=campaign_ids, status=ServiceStatus.DELETE.value)