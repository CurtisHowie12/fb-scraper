"""Registry of Facebook Ads Library URLs to scrape, grouped by site/client name.

Add a new client by adding a key with a list of one or more ads-library URLs.
"""

WEBSITES: dict[str, list[str]] = {
    "carpe": [
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=315614678610514",
    ],
    "test website": [
        "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&is_targeted_country=false&media_type=all&search_type=page&sort_data[direction]=desc&sort_data[mode]=total_impressions&view_all_page_id=315614678610514",
    ],
}
