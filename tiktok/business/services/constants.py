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
from enum import Enum

BASE_URL = os.environ.get("BASE_URL", "https://google.com/")
VERSION = os.environ.get("VERSION", "v1.2")

class Urls(Enum):
    # Campaign
    CAMPAIGN_BASE_URL = BASE_URL + VERSION + "/campaign/"
    CAMPAIGN_GET_URL = CAMPAIGN_BASE_URL + "get/"
    CAMPAIGN_CREATE_URL = CAMPAIGN_BASE_URL + "create/"
    CAMPAIGN_UPDATE_URL = CAMPAIGN_BASE_URL + "update/"
    CAMPAIGN_UPDATE_STATUS_URL = CAMPAIGN_UPDATE_URL + "status/"
