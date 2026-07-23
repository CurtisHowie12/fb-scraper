import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def scrape_ads_library(url: str, data_limit: int | None = 10, headless: bool = False) -> list[dict]:
    """
    Scrape a Facebook Ads Library search results page.

    url: the ads-library URL to visit.
    data_limit: set to an integer to stop after that many ads, or None to
        scrape everything the page reports.
    headless: run Chrome headless (needed in CI where there is no display).
    """

    # Set Chrome options for headless mode
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless=new')
    else:
        chrome_options.add_argument('--start-maximized')

    # Initialize the webdriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the website
        driver.get(url)

        time.sleep(6)

        results = driver.find_element(
            "xpath",
            './/div[@class="x8t9es0 x1uxerd5 xrohxju x108nfp6 xq9mrsl x1h4wwuj x117nqv4 xeuugli"]'
        ).text

        total_results = int(
            results.replace('~', '')
                   .replace(',', '')
                   .replace(' results', '')
        )

        # Scroll only when needed
        while True:

            compare_result = driver.find_elements(
                "xpath",
                '(//div[@class="x1plvlek xryxfnj x1gzqxud x178xt8z x1lun4ml xso031l xpilrb4 xb9moi8 xe76qn7 x21b0me x142aazg x1i5p2am x1whfx0g xr2y4jy x1ihp6rs x1kmqopl x13fuv20 x18b5jzi x1q0q8m5 x1t7ytsu x9f619"]//div[@class="xh8yej3"])'
            )

            loaded_result = int(len(compare_result))

            # If user only wants a limited amount
            if data_limit is not None:
                if loaded_result >= data_limit:
                    break

            # If user wants everything
            else:
                if loaded_result >= total_results:
                    break

            previous_loaded = loaded_result

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            compare_result = driver.find_elements(
                "xpath",
                '(//div[@class="x1plvlek xryxfnj x1gzqxud x178xt8z x1lun4ml xso031l xpilrb4 xb9moi8 xe76qn7 x21b0me x142aazg x1i5p2am x1whfx0g xr2y4jy x1ihp6rs x1kmqopl x13fuv20 x18b5jzi x1q0q8m5 x1t7ytsu x9f619"]//div[@class="xh8yej3"])'
            )

            loaded_result = int(len(compare_result))

            # No more ads are loading
            if loaded_result == previous_loaded:
                break

        compare_result = driver.find_elements(
            "xpath",
            '(//div[@class="x1plvlek xryxfnj x1gzqxud x178xt8z x1lun4ml xso031l xpilrb4 xb9moi8 xe76qn7 x21b0me x142aazg x1i5p2am x1whfx0g xr2y4jy x1ihp6rs x1kmqopl x13fuv20 x18b5jzi x1q0q8m5 x1t7ytsu x9f619"]//div[@class="xh8yej3"])'
        )

        loaded_result = int(len(compare_result))

        if data_limit is not None:
            compare_result = min(data_limit, loaded_result)
        else:
            compare_result = loaded_result

        collected_data = []

        for i in range(compare_result):      # <-- Number of ads to capture

            first_layer = driver.find_element("xpath", f'(//div[@class="xdj266r x11t971q xat24cr xvc5jky x1dr75xp xh8yej3 xkopdvs"]//div[@class="xh8yej3"])[{i+1}]')

            try:
                poster_name = first_layer.find_element("xpath", './/a[contains(@href,"facebook.com")]').text
            except NoSuchElementException:
                poster_name = None

            try:
                poster_url = first_layer.find_element("xpath", './/a[contains(@href,"facebook.com")]').get_attribute("href")
            except NoSuchElementException:
                poster_url = None

            posted_with = None
            posted_withs = first_layer.find_elements("xpath", './/*[contains(text(),"with")]')
            if posted_withs:
                posted_with = posted_withs[0].text

            try:
                body_text = first_layer.find_element("xpath", './/div[@style="white-space: pre-wrap;"]').get_attribute("innerText")
            except NoSuchElementException:
                body_text = None

            try:
                media_url = first_layer.find_element(
                    "xpath",
                    './/div[@class="x5yr21d x1uhb9sk xh8yej3"]//video | .//div[@class="x1ywc1zp x78zum5 xl56j7k x1e56ztr x1277o0a"]//img'
                ).get_attribute("src")
            except NoSuchElementException:
                media_url = None

            try:
                shop_now_url = first_layer.find_element("xpath", './/a[@class="x1hl2dhg x1lku1pv x8t9es0 x1fvot60 xxio538 xjnfcd9 xq9mrsl x1yc453h x1h4wwuj x1fcty0u x1lliihq"]').get_attribute("href")
            except NoSuchElementException:
                shop_now_url = None

            try:
                headline = first_layer.find_element("xpath", './/div[@class="x6ikm8r x10wlt62 xlyipyv x1mcwxda x190qgfh"]').text
            except NoSuchElementException:
                headline = None

            viewmores = driver.find_elements(
                "xpath",
                '//div[text()="See summary details" or text()="See ad details"]'
            )

            if i >= len(viewmores):
                break

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", viewmores[i])
            driver.execute_script("arguments[0].click();", viewmores[i])

            time.sleep(1)

            data_to_gets = driver.find_elements(
                "xpath",
                '''
                //div[@class="xt9c220 x1sdr0u7 x1on1db2 xrvj5dj xmz0i5r"]
                  //div[@class="x1cy8zhl x78zum5 xyamay9 xv54qhq x18d9i69 xf7dkkf x1n2onr6"]
                  //div[@class="x78zum5 xdt5ytf x2lwn1j xeuugli"]
                |
                (//div[@class="xyamay9 xv54qhq x1l90r2v xf7dkkf x106t9lo xmd1z x1gzqxud x1i5p2am x1whfx0g xr2y4jy x1ihp6rs"]
                  //div[@class="x78zum5 xdt5ytf x2lwn1j xeuugli"])[1]
                '''
            )

            if not data_to_gets:
                ad_data = {
                    "poster_name": poster_name,
                    "poster_url": poster_url,
                    "posted_with": posted_with,
                    "body_text": body_text,
                    "media_url": media_url,
                    "shop_now_url": shop_now_url,
                    "headline": headline,
                    "status": None,
                    "library_id": None,
                    "started_running": None,
                    "platforms": [],
                    "multiple_versions": False
                }
                collected_data.append(ad_data)

            for data_to_get in data_to_gets:

                lines = data_to_get.text.split("\n")

                ad_data = {
                    "poster_name": poster_name,
                    "poster_url": poster_url,
                    "posted_with": posted_with,
                    "body_text": body_text,
                    "media_url": media_url,
                    "shop_now_url": shop_now_url,
                    "headline": headline,
                    "status": None,
                    "library_id": None,
                    "started_running": None,
                    "platforms": [],
                    "multiple_versions": False
                }

                for line in lines:

                    line = line.strip()

                    if line == "Active":
                        ad_data["status"] = line

                    elif line.startswith("Library ID:"):
                        ad_data["library_id"] = line.replace("Library ID:", "").strip()

                    elif line.startswith("Started running on"):
                        ad_data["started_running"] = line.replace("Started running on", "").strip()

                    elif line == "Platforms":
                        platform_map = {
                            "0px -955px": "Facebook",
                            "0px -1007px": "Instagram",
                            "-388px -732px": "Audience Network",
                            "-387px -753px": "Messenger",
                            "-387px -766px": "Threads"
                        }

                        ad_data["platforms"] = []

                        icons = data_to_get.find_elements(
                            "xpath",
                            './/div[contains(@style,"mask-position")]'
                        )

                        for icon in icons:

                            style = icon.get_attribute("style")

                            for position, platform in platform_map.items():
                                if f"mask-position: {position}" in style:
                                    ad_data["platforms"].append(platform)
                                    break

                    elif "multiple versions" in line.lower():
                        ad_data["multiple_versions"] = True

                collected_data.append(ad_data)

            try:
                close = driver.find_element(
                    "xpath",
                    '//*[@id="facebook"]/body/div[6]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/span/div/span/div/div[2]/div/div'
                )
            except NoSuchElementException:
                close = None

        #     driver.execute_script("arguments[0].click();", close)
            print(f"Done scraping ad page {i+1}")
            time.sleep(1)

        return collected_data

    finally:
        driver.quit()
