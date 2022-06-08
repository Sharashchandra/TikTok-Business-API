# TikTok Business API Wrapper

# Installation

``` console
pip install TikTok-Business-API
```

The current version of this package only covers the Tiktok Business API. Tiktok Developer API support will be added in a later version.

# Getting Started

To get started, get an Access Token from the app detail page in the [TikTok for Business Developers page](https://ads.tiktok.com/marketing_api/apps/).
You can also use the access token from the sandbox account to make test calls to the sandbox account.

# Authorization

Obtaining an access_token is simple. Visit the authorization url mentioned in the app detail page. Once you login and grant authorization, it will redirect you to the callback url mentioned while creating the app. The auth_code can be gotten from url after the callback.

By default, the access token will be written to `~/.tiktok/access_token.json`

``` python
from tiktok.business.oauth2 import OAuth

access_token = OAuth2.get_access_token(
    app_id='YOUR_APP_ID',
    secret='YOUR_APP_SECRET',
    auth_code='AUTH_CODE FROM CALLBACK',
    write_to_file=True,
    file_path="access_token.json"
)
```
# Usage Documentation

This api wrapper makes it easy to switch between the main app and the sandbox account. This client will automatically include the advertiser id to every request if not specified otherwise.The Access Token is included in the header for all the api calls made.

You can initialize a new `Client` by making use of the `access_token.json` file generated in the previous step. The access tokens will be loaded in from `~/.tiktok/access_token.json` if path is not mentioned. Advertiser Id can also added to the `access_token.json`.

``` python
from tiktok.business.client import TikTokBusinessClient

client = TikTokBusinessClient.from_json_file(
    json_file_path="/path/to/file",
    sandbox=True
)
```

You can initialize a new `Client` with just the Access Token and Advertiser Id to get started.

``` python
from tiktok.business.client import TikTokBusinessClient

client = TikTokBusinessClient(
    access_token='YOUR_ACCESS_TOKEN',
    advertiser_id='AD_ADVERTISER_ID'
)
```

You can also create a new `Client` for the sandbox account in the same way

``` python
from tiktok.business.client import TikTokBusinessClient

client = TikTokBusinessClient(
    access_token='SANDBOX_ACCESS_TOKEN',
    advertiser_id='SANDBOX_ADVERTISER_ID',
    sandbox=True
)
```

The actual function calls remain the same with the only difference being in the url. URLs:

* SANDBOX_URL = https://sandbox-ads.tiktok.com/open_api
* BUSINESS_URL = https://business-api.tiktok.com/open_api

All the functionality of the modules can be accessed as attributes of the client object. The functions for each module differs and follows the [TikTok Business API Documentation](https://ads.tiktok.com/marketing_api/docs)

``` python
from tiktok.business.client import TikTokBusinessClient

client = TikTokBusinessClient.from_json_file(
    json_file_path="/path/to/file",
    sandbox=True
)

# Get all campaigns
campaigns = client.campaign.get_campaign()

# Create ad
ad_params = {...}
ad = client.ad.create_ad(ad_params)
```
