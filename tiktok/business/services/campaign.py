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
from tiktok.business.services.constants import ServiceStatus


class Campaign:
    def __init__(self, client):
        self.client = client
        self.campaign_base_url = self.client.build_url(self.client.base_url, "campaign/")

    def get_campaigns(self, params=None):
        url = self.client.build_url(self.campaign_base_url, "get/")
        return self.client.make_paginated_request(url, params=params or {})

    def create_campaign(self, data=None):
        url = self.client.build_url(self.campaign_base_url, "create/")
        return self.client.post(url, data=data or {})

    def update_campaign(self, data=None):
        url = self.client.build_url(self.campaign_base_url, "update/")
        return self.client.post(url, data=data or {})

    def _update_campaign_status(self, campaign_ids, status):
        campaign_ids = [campaign_ids] if isinstance(campaign_ids, str) else campaign_ids
        data = {"campaign_ids": campaign_ids, "operation_status": status}
        url = self.client.build_url(self.campaign_base_url, "status/update/")
        return self.client.post(url, data=data)

    def enable_campaigns(self, campaign_ids):
        return self._update_campaign_status(campaign_ids=campaign_ids, status=ServiceStatus.ENABLE.value)

    def disable_campaigns(self, campaign_ids):
        return self._update_campaign_status(campaign_ids=campaign_ids, status=ServiceStatus.DISABLE.value)

    def delete_campaigns(self, campaign_ids):
        return self._update_campaign_status(campaign_ids=campaign_ids, status=ServiceStatus.DELETE.value)
