import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from myhome.listings.customs.getInsideData import scrape_property_info


def startBot(token):

    driver = webdriver.Chrome()

    # URL pattern
    url_pattern = ("https://www.myhome.ge/ka/s/?Keyword=%E1%83%97%E1%83%91%E1%83%98%E1%83%9A%E1%83%98%E1%83%A1%E1%83%98"
                   "&AdTypeID=1&PrTypeID=1.2&regions=1.2.3.4.5.6&fullregions=6&districts=1.2.3.4.5.6.7.8.9.10.11.12.118"
                   ".13.14.15.16.17.18.19.20.21.22.68.69.70.102.103.23.24.25.26.27.106.111.28.29.30.38.39.40.41.42.43.44"
                   ".45.46.47.48.101.117.49.50.51.52.53.54.55.56.57.58.59.60.78.107.61.62.63.64.65.66.67&cities=1"
                   "&OwnerTypeID=1&Ajax=1")

    # Start from page 1
    page_num = 1

    # Initialize counter for number of IDs
    total_ids = 0

    # Iterate through pages until the last page is reached
    while True:
        # Construct URL for the current page
        url = url_pattern.format(page_num)
        driver.get(url)

        # Wait for 0.5 seconds
        time.sleep(0.5)

        # Find all listing elements
        listings = driver.find_elements(By.XPATH,
                                        '//a[@class="outline-none group relative flex h-[200px] w-full overflow-hidden '
                                        'rounded-xl border border-gray-20 py-4 pl-4 transition-all duration-500 '
                                        'lg:hover:shadow-devCard"]')

        # If there are no listings found, it's the last page
        if len(listings) == 0:
            break

        # Extract and save IDs
        for listing in listings:
            href = listing.get_attribute("href")
            # Use regular expressions to extract the ID part from the URL
            match = re.search(r'/pr/(\d+)/', href)
            if match:
                listing_id = match.group(1)
                url = f"https://www.myhome.ge/ka/pr/{listing_id}"
                orders1 = scrape_property_info(url)

                orders1["listing_id"] = listing_id
                orders1["is_already_listed"] = False
                orders1["ProductTypeID"] = "1"
                orders1["loc_city"] = "1"

                orders1["loc_city_title_ka"] = "თბილისი"

                orders1["loc_city_title_en"] = "თბილისი"

                orders1["loc_city_title_ru"] = "თბილისი"

                orders1["loc_city_seo_title_ka"] = "თბილისში"

                orders1["loc_city_seo_title_en"] = "თბილისში"

                orders1["loc_city_seo_title_ru"] = "თბილისში"

                orders1["IsDev"] = "0"

                orders1["Phone"] = "591082493"

                orders1["phoneIsActive"] = "1"

                orders1["PromBlockAutoUpdateHour"] = "0"

                orders1["PromBlockAutoUpdateQuantity"] = "1"

                orders1["aupdate_packet"] = "0"

                orders1["PromBlockColorQuantity"] = "0"

                orders1["color_packet"] = "0"

                orders1["vip_packet"] = "0"

                orders1["StreetAddr"] = ""

                orders1["loc_street"] = "1"

                orders1["vip_plus_packet"] = "0"

                orders1["PromBlockVipQuantity"] = "0"

                orders1["CadCode"] = ""

                orders1["super_vip_packet"] = "1"

                orders1["ChangeInfo"] = ""

                orders1["ProductOwner"] = "Tbilisi"

                orders1["PaymentMethod"] = "balance"

                orders1["PayWithCard"] = "0"

                orders1["CurrencyID"] = "3"

                orders1["UserEmail"] = "tarielinvest@gmail.com"

                orders1["draftId"] = "6167953"

                orders1["PrID"] = ""
                orders1["Code"] = ""

                orders1["IP"] = "87.253.53.94"

                print(token)

                # upload_listing_for_sale(orders1, token)
                time.sleep(5)

                print('order added')
        # Move to the next page
        page_num += 1

    print("test")
    driver.quit()

    print("Total number of IDs:", total_ids)

    return
