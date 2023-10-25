# TikTok Business API Wrapper

This is a minimal api wrapper to interface with the Tiktok business API

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
from tiktok.business.oauth2 import OAuth2

access_token = OAuth2.get_access_token(
    app_id='YOUR_APP_ID',
    secret='YOUR_APP_SECRET',
    auth_code='AUTH_CODE FROM CALLBACK',
    write_to_file=True,
    file_path="access_token.json"
)
```
# Initializing a client

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

# Endpoints

All the functionality of the modules can be accessed as attributes of the client object. The functions for each module differs and follows the [TikTok Business API Documentation](https://ads.tiktok.com/marketing_api/docs)

Follow the steps outlined here to [create a client object](#Initializing-a-client)

All of the GET/LIST functions take the same parameters `params` and all the POST methods take `data` as mentioned in the official documentation unless specified.

The client object keeps a track of the advertiser id and passes it along with each request. There is no need to explicitly pass it in the params.

## Campaign
``` python
# Get campaigns (page_size set to 1000 by default)
client.campaign.get_campaigns(params)

# Create campaign
client.campaign.create_campaigns(data)

# Update campaign
client.campaign.update_campaign(data)

# Enable campaigns (max allowed 100 campaign ids in a single request)
client.campaign.enable_campaigns(campaigns_ids: List[str])

# Disable campaigns (max allowed 100 campaign ids in a single request)
client.campaign.disable_campaigns(campaigns_ids: List[str])

# Delete campaigns (max allowed 100 campaign ids in a single request)
client.campaign.delete_campaigns(campaigns_ids: List[str])
```

## Ad Group
``` python
# Get ad groups (page_size set to 1000 by default)
client.ad_group.get_ad_groups(params)

# Create ad group
client.ad_group.create_ad_group(data)

# Update ad group
client.ad_group.update_ad_group(data)

# Update ad group budget
client.ad_group.update_ad_group_budget(data)

# Enable ad groups (max allowed 100 adgroup_ids in a single request)
client.ad_group.enable_adgroups(adgroups_ids: List[str])

# Disable adgroups (max allowed 100 adgroup_ids in a single request)
client.ad_group.disable_adgroups(adgroups_ids: List[str])

# Delete adgroups (max allowed 100 adgroup_ids in a single request)
client.ad_group.delete_adgroups(adgroups_ids: List[str])
```

## Ad
``` python
# Get ads (page_size set to 1000 by default)
client.ad.get_ads(params)

# Create ad
client.ad.create_ad(data)

# Update ad
client.ad.update_ad(data)

# Enable ads (max allowed 100 ad_ids in a single request)
client.ad.enable_ads(ads_ids: List[str])

# Disable ads (max allowed 100 ad_ids in a single request)
client.ad.disable_ads(ads_ids: List[str])

# Delete ads (max allowed 100 ad_ids in a single request)
client.ad.delete_ads(ads_ids: List[str])
```

## Creative
### Image
``` python
# Upload image file
client.creative.image.upload_file(file_path: str, file_name: Optional[str])

# Upload file by url
client.creative.image.upload_file_by_url(url: str, file_name: Optional[str])

# Upload file by file id
client.creative.image.upload_file_by_file_id(file_id: str, file_name: Optional[str])
```

### Video
``` python
# Upload video file
client.creative.video.upload_file(file_path: str, file_name: Optional[str])

# Upload file by url
client.creative.video.upload_file_by_url(url: str, file_name: Optional[str])

# Upload file by file id
client.creative.video.upload_file_by_file_id(file_id: str, file_name: Optional[str])
```

### Music
``` python
# Upload music file
client.creative.music.upload_file(file_path: str, file_name: Optional[str])

# Upload file by url
client.creative.music.upload_file_by_url(url: str, file_name: Optional[str])

# Upload file by file id
client.creative.music.upload_file_by_file_id(file_id: str, file_name: Optional[str])
```

## Audience
``` python
# Get all audiences (page_size set to 1000 by default)
client.audience.get_all_audiences(params)

# Get audience details (max allowed 100 custom_audience_ids in a single request)
client.audience.get_audience_details(custom_audience_ids: List[str])

# Upload audience (each file needs to be less 50 mb. will add functionality to handle bigger file sizes in future release)
client.audience.upload_audience(file_path: str, calculate_type: str)

# Create custom audience by tiktok file paths
client.audience.create_audience_by_file(data)

# Create custom audience by rules
client.audience.create_audience_by_rule(data)

# Create lookalike audience by file_ids
client.audience.create_lookalike_audience(data)

# Update custom audience
client.audience.update_audience(data)

# Delete custom audience (max allowed 100 custom_audience_ids in a single request)
client.audience.delete_audience(custom_audience_ids: List[str])

# Share custom audience with advertiser accounts
client.audience.share_audience(data)

# Cancel audience sharing (currently an allowlist-only feature)
client.audience.cancel_audience_sharing(data)

# Get audience share log (currently an allowlist-only feature)
client.audience.get_audience_sharing_log(custom_audience_id: str)
```

## Reports
``` python
# Get synchronous report (page_size set to 1000 by default)
client.reports.get_synchronous_report(params)

# Create asynchronous report task (page_size set to 1000 by default) (currently an allowlist-only feature)
client.reports.create_asynchronous_report_task(data)

# Check asynchronous report task
client.reports.check_asynchronous_report_task(task_id: str)

# Download asynchronous report
client.reports.download_asynchronous_report(task_id: str, file_path: str)
```
