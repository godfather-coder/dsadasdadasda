import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from .addListing import upload_listing_for_sale
from .getInsideData import scrape_property_info
from django.contrib.auth import get_user_model

from ..models import Listing

User = get_user_model()


def startBot(token, user):

    number = user.phone_number
    driver = webdriver.Chrome()

    url_pattern = ("https://www.myhome.ge/ka/s/?Keyword=%E1%83%97%E1%83%91%E1%83%98%E1%83%9A%E1%83%98%E1%83%A1%E1%83%98"
                   "&AdTypeID=1&PrTypeID=1.2&regions=1.2.3.4.5.6&fullregions=6&districts=1.2.3.4.5.6.7.8.9.10.11.12.118"
                   ".13.14.15.16.17.18.19.20.21.22.68.69.70.102.103.23.24.25.26.27.106.111.28.29.30.38.39.40.41.42.43.44"
                   ".45.46.47.48.101.117.49.50.51.52.53.54.55.56.57.58.59.60.78.107.61.62.63.64.65.66.67&cities=1"
                   "&OwnerTypeID=1&Ajax=1")

    # Start from page 1
    page_num = 1

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
            if User.objects.get(phone_number=number).botStatus is False:
                driver.quit()
                return
            href = listing.get_attribute("href")
            # Use regular expressions to extract the ID part from the URL
            match = re.search(r'/pr/(\d+)/', href)
            print(match)
            if match:
                listing_id = match.group(1)
                print(listing_id)
                if Listing.objects.filter(listing_id=listing_id, users=user).exists():
                    print("ისკიპება")
                    continue
                orders1 = scrape_property_info(listing_id, user)
                upload_listing_for_sale(orders1, token, user)

        # Move to the next page
        page_num += 1

    driver.quit()