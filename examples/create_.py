from tiktok.business.client import TikTokBusinessClient

client = TikTokBusinessClient(access_token="XXX", advertiser_id="XXX")

response = client.campaign.create_campaign({
    "campaign_name": f"test_campaign",
    "objective_type": "TRAFFIC",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": "50.0",
})

campaign_id = response["data"]["campaign_id"]

response = client.ad_group.create_ad_group({
    "campaign_id": campaign_id,
    "adgroup_name": f"test_ad_group",
    "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
    "placement": ["PLACEMENT_TIKTOK"],
    "external_type": "WEBSITE",
    "location": ["5879092"],
    "operation_system": ["ANDROID"],
    "budget": "140.0",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "2022-06-10 11:12:13",
    "schedule_end_time": "2022-06-17 11:12:13",
    "optimize_goal": "CLICK",
    "pacing": "PACING_MODE_SMOOTH",
    "billing_event": "CPC",
    "bid_type": "BID_TYPE_NO_BID",
})

adgroup_id = response["data"]["adgroup_id"]

image_id = "ad-site-i18n-sg/202206065d0d18471b5934664bd7940a"

response = client.ad.create_ad({
    "adgroup_id": adgroup_id,
    "creatives": [{
        "adgroup_id": adgroup_id,
        "call_to_action": "CONTACT_US",
        "ad_name": f"test_ad",
        "image_ids": [image_id],
        "ad_format": "SINGLE_IMAGE",
        "ad_text": f"test_ad_text",
        "landing_page_url": "https://www.google.com",
        "display_name": "This is a test ad"
    }]
})
ad_id = response["data"]["ad_ids"][0]

print(campaign_id, adgroup_id, image_id, ad_id)
print("-*-"*10)