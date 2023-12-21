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
class Identity:
    def __init__(self, client):
        self.client = client
        self.identity_base_url = self.client.build_url(self.client.base_url, "identity/")

    def get_identities(self, params=None):
        url = self.client.build_url(self.identity_base_url, "get/")
        return self.client.make_paginated_request(url, params=params or {"page_size": 100})

    def get_identity(self, identity_name, params=None):
        filtering = {"filtering": {"keyword": identity_name}}
        if params:
            params.update(filtering)
        else:
            params = {**filtering, "page_size": 100}
        url = self.client.build_url(self.identity_base_url, "get/")
        return self.client.make_paginated_request(url, params=params or {})

    def get_identity_info(self, params=None):
        url = self.client.build_url(self.identity_base_url, "info/")
        return self.client.make_paginated_request(url, params=params or {})

    def get_videos_under_identity(self, params=None):
        url = self.client.build_url(self.identity_base_url, "video/get/")
        return self.client.make_paginated_request(url, params=params or {})

    def get_posts_under_identity(self, params=None):
        url = self.client.build_url(self.identity_base_url, "video/info/")
        return self.client.make_paginated_request(url, params=params or {})

    def get_music_authorisation_info(self, params=None):
        url = self.client.build_url(self.identity_base_url, "music/authorization/")
        return self.client.make_paginated_request(url, params=params or {})

    def create_identity(self, data=None):
        url = self.client.build_url(self.identity_base_url, "create/")
        return self.client.post(url, data=data or {})

    def delete_identity(self, data=None):
        url = self.client.build_url(self.identity_base_url, "delete/")
        return self.client.post(url, data=data or {})
