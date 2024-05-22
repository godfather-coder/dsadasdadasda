import re
import json
import requests
from django.http import JsonResponse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .aa import decode_title
from .locations import get_locs
from ..models import Listing


def scrape_property_info(listing_id, data):
    print(listing_id)
    email = data.email
    phone_number = data.phone_number

    if Listing.objects.filter(listing_id=listing_id, users=data).exists():
        print("განცხადება ამ აიდით დევს, ისკიპება")

    driver = webdriver.Chrome()
    driver.get("https://www.myhome.ge/ka/pr/"+listing_id)



    try:
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@class, 'hover-underline') and text()='მეტის ნახვა']"))
        )
        more_button.click()
    except Exception as e:
        pass

    # Wait for the amenities to load

    # Find the statement title

    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".statement-title h1"))
    )

    # Once the element is visible, retrieve its text
    h1_text = element.text

    # Find the address
    address_element = driver.find_element(By.CLASS_NAME, "address")
    address = address_element.text

    address_array = address.split(", ")

    def map_local(word):
        mappings = {
            "გლდანი-ნაძალადევი": "1",
            "თბილისის შემოგარენი": "2",
            "დიდუბე-ჩუღურეთი": "3",
            "ვაკე-საბურთალო": "4",
            "ისანი-სამგორი": "5",
            "ძველი თბილისი": "6",

        }
        return mappings.get(word, "Unknown")

    def map_seo_ka(word):
        mappings = {
            "გლდანი-ნაძალადევი": "გლდანი-ნაძალადევში",
            "თბილისის შემოგარენი": "თბილისის შემოგარენში",
            "დიდუბე-ჩუღურეთი": "დიდუბე-ჩუღურეთში",
            "ვაკე-საბურთალო": "ვაკე-საბურთალოში",
            "ისანი-სამგორი": "ისანი-სამგორში",
            "ძველი თბილისი": "ძველ თბილისში",

        }
        return mappings.get(word, "Unknown")

    keyword_objects = []

    def generate_keyword_objects():
        keywords = {
            "loc_district_title_ka": address_array[-2],
            "loc_district_title_en": address_array[-2],
            "loc_district_title_ru": address_array[-2],
            "loc_district_seo_title_ka": map_seo_ka(address_array[-2]),
            "loc_district_seo_title_en": map_seo_ka(address_array[-2]),
            "loc_district_seo_title_ru": map_seo_ka(address_array[-2]),
            "loc_urban_title_ka": address_array[-3],
            "loc_urban_title_en": address_array[-3],
            "loc_urban_title_ru": address_array[-3],
            "loc_district": map_local(address_array[-2]),
            "loc_street_title_ka": address_array[0],
            "loc_street_title_en": address_array[0],
            "loc_street_title_ru": address_array[0]

        }
        # Return each keyword as a separate object

        for key, value in keywords.items():
            keyword_object = {key: value}
            keyword_objects.append(keyword_object)
        return keyword_objects

    generate_keyword_objects()

    # Find the comment
    try:
        comment_element = driver.find_element(By.CLASS_NAME, "pr-comment")
        comment = comment_element.text
    except NoSuchElementException:
        comment = None  # or any default value you prefer

    # Find all main features divs
    main_features_divs = driver.find_elements(By.CLASS_NAME, "main-features")
    main_features_values = []
    for div in main_features_divs:
        spans = div.find_elements(By.XPATH, ".//span[contains(@class, 'd-block')]")
        for span in spans:
            main_features_values.append(span.text.strip())

    # Find all d-block elements under amenities-ul
    amenities_uls = driver.find_elements(By.CLASS_NAME, "amenities-ul")
    amenities_first = []
    amenities_second = []
    for index, ul in enumerate(amenities_uls):
        li_elements = ul.find_elements(By.TAG_NAME, "li")
        for li in li_elements:
            div_element = li.find_element(By.TAG_NAME, "div")
            span_elements = div_element.find_elements(By.CLASS_NAME, "d-block")
            amenities_data = [span_element.text for span_element in span_elements if
                              'no' not in span_element.get_attribute('class')]
            if index == 0:
                amenities_first.append(amenities_data)
            elif index == 1:
                amenities_second.extend(amenities_data)  # Change append to extend

    # Find the price
    price_element = driver.find_element(By.XPATH,
                                        "//span[contains(@class, 'd-block') and contains(@class, 'convertable')]")
    price_gel = price_element.get_attribute("data-price-gel")
    price_usd = price_element.get_attribute("data-price-usd")
    price_gel = price_gel.replace(",", "")

    # Find the area
    area_element = driver.find_element(By.XPATH,
                                       "//span[text()='ფართი:']/ancestor::div[@class='space d-flex align-items-center']/div")
    area_text = area_element.text.strip()  # Extracting the text
    area_value = re.search(r'(\d+(\.\d+)?)', area_text).group(1)  # Extracting only the numeric part

    # Find the latitude and longitude
    try:
        map_div = driver.find_element(By.ID, "map")
        lat = map_div.get_attribute("data-lat")
        lng = map_div.get_attribute("data-lng")
        zoom = map_div.get_attribute("data-zoom")
    except NoSuchElementException:
        lat = None
        lng = None
        zoom = None

    # Find all image elements
    image_elements = driver.find_elements(By.XPATH, '//div[@class="swiper-thumbs"]//img')

    word = "youtube"
    images = []
    for img in image_elements:
        img_url = img.get_attribute("data-src")
        if img_url and not word in img_url:
            images.append(img_url)


    def upload_images(image_urls):

        for index, image_url in enumerate(image_urls):
            response = requests.get(image_url)
            if response.status_code == 200:
                image_blob = response.content

                # Try using a different image format
                image_format = 'image/jpeg' if image_url.lower().endswith('.jpg') or image_url.lower().endswith(
                    '.jpeg') else 'image/png'
                files = {'Files[]': ('image.jpg', image_blob, image_format)}
                data = {
                    'Func': 'UploadPhotos',
                    'UploadedFiles': str(index),
                    'IP': '87.253.53.94',
                    'SiteID': '4'
                }

                upload_url = "https://static.my.ge/"
                headers = {
                    'Content-Type': 'multipart/form-data'
                }
                upload_response = requests.post(upload_url, files=files, data=data, headers=headers)
                if upload_response.status_code == 200:
                    try:
                        upload_data = upload_response.json()
                        uploaded_image_url = upload_data['Data']['FilesList'][0]
                        images.append(uploaded_image_url)
                    except (ValueError, KeyError) as e:
                        return JsonResponse({'error': 'Failed to parse upload response'}, status=500)
                else:
                    return JsonResponse({'error': 'Failed to upload image'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to fetch image'}, status=500)

        return images

    images = upload_images(images)
    # Define a dictionary to map extracted amenities to desired values
    amenity_mapping = {
        "ახალი გარემონტებული": {"ConditionID": "1"},
        "მიმდინარე რემონტი": {"ConditionID": "4"},
        "სარემონტო": {"ConditionID": "5"},
        "ძველი გარემონონტებული": {"ConditionID": "6"},
        "თეთრი კარკასი": {"ConditionID": "7"},
        "შავი კარკასი": {"ConditionID": "8"},
        "მწვანე კარკასი": {"ConditionID": "9"},
        # -------
        "არასტანდარტული": {"ProjectID": "1"},
        "თუხარელის": {"ProjectID": "2"},
        "მოსკოვის": {"ProjectID": "3"},
        "ქალაქური": {"ProjectID": "4"},
        "ხრუშოვის": {"ProjectID": "5"},
        "ჩეხური": {"ProjectID": "6"},
        "ყავლაშვილის": {"ProjectID": "7"},
        "ლვოვის": {"ProjectID": "8"},
        "თბილისური ეზო": {"ProjectID": "9"},
        # --------
        "ლოჯი": {"Loggia": "1"},
        "გათბობა": {"WarmingID": "1"},
        "ცენტრალური გათბობა": {"Amenities": "Central Heating"},
        "პარკინგი": {"ParkingID": "1"},
        "ცხელი წყალი": {"HotWaterID": "1"},
        "სათავსო": {"StoreType": "1"},
        "კონდიციონერი": {"Conditioner": "3"},
        "შშმპ ადაპტირებული": {"SpecialPersons": "1"},
        "ბუნებრივი აირი": {"Gas": "1"},
        "სიგნალიზაცია": {"Alarm": "342"},
        "მისაღები": {"LivingRoom": "342"},
        "ინტერნეტი": {"Internet": "410"},
        "ბუხარი": {"FirePlace": "184"},
        "ავეჯი": {"HasFurnitureAndTechnic": "1"},
        "სამგზავრო ლიფტი": {"Elevator1": "343"},
        "სატვირთო ლიფტი": {"Elevator2": "344"},
        "ტელეფონი": {"Telephone": "1"},
        "ტელევიზორი": {"TV": "2"},
        "აუზი": {"PoolType": "1"},
        "მაცივარი": {"Refrigerator": "358"},
        "სარეცხი მანქანა": {"WashingMachine": "359"},
        "ჭურჭლის სარეცხი მანქანა": {"Dishwasher": "360"},
        "ქურა (გაზის/ელექტრო)": {"Curry": "361"},
        "ღუმელი": {"Furnace": "362"},
    }

    # Map extracted amenities to desired values
    mapped_amenities_first = []
    for amenities_group in amenities_first:
        mapped_group = {}
        for amenity in amenities_group:
            mapped_amenity = amenity_mapping.get(amenity)
            if mapped_amenity is None:
                # Check if it's Rooms, CeilingHeight, or a combination of Balcony and BalconySize
                if "საძინებელი" in amenity or "ჭერის სიმაღლე" in amenity:
                    number_match = re.search(r'(\d+(\.\d+)?)', amenity)
                    if number_match:
                        mapped_group["Rooms" if "საძინებელი" in amenity else "CeilingHeight"] = number_match.group(1)
                elif "აივანი" in amenity:
                    # Check if the amenity includes size information
                    size_match = re.search(r'(\d+(\.\d+)?)\s*მ²', amenity)
                    if size_match:
                        mapped_group["Balcony"] = "1"
                        mapped_group["BalconySize"] = size_match.group(1)
                    else:
                        mapped_group["Balcony"] = "1"
                # Fallback to original amenity if not mapped
                elif "ვერანდა" in amenity:
                    # Check if the amenity includes size information
                    size_match = re.search(r'(\d+(\.\d+)?)\s*მ²', amenity)
                    if size_match:
                        mapped_group["Veranda"] = "1"
                        mapped_group["VerandaSize"] = size_match.group(1)
                    else:
                        mapped_group["Veranda"] = "1"
                elif "სველი წერტილი" in amenity:
                    number_match = re.search(r'სველი წერტილი (\d+)', amenity)
                    if number_match:
                        mapped_group["BathRooms"] = number_match.group(1)
                # Fallback to original amenity if not mapped
                else:
                    mapped_group["Amenities"] = amenity
            else:
                mapped_group.update(mapped_amenity)
        mapped_amenities_first.append(mapped_group)

    mapped_amenities_second = []
    for amenity in amenities_second:
        mapped_amenity = amenity_mapping.get(amenity)
        if mapped_amenity is None:
            mapped_amenity = {"Amenities": amenity}  # Return original amenity if not mapped
        mapped_amenities_second.append(mapped_amenity)

    # Create a dictionary with the extracted information
    pattern = r'(\d*\.?\d+)(?:\s*მ²)?'  # Assuming this pattern is used to extract the area information
    match = re.search(pattern, main_features_values[0])

    upper_floor = None
    lower_floor = None
    try:
        if '/' in main_features_values[4]:
            upper_floor, lower_floor = main_features_values[4].split('/')
    except Exception as e:
        pass

    additional_data = decode_title(h1_text)

    split_address = address.split(', ')
    reversed_address = split_address[::-1]

    reversed_address = ', '.join(reversed_address)

    property_info = {
        "Keyword": reversed_address,
        "CommentGeo": comment,
        "CommentEng": comment,
        "CommentRus": comment,
        "VideoUrl": "",
        "MaklerId": "",
        "loc_urban": get_locs(address_array[-3]),

        "AreaSize": float(match.group(1)) if match else None,
        "BedRooms": main_features_values[2] if len(main_features_values) > 2 else None,
        "Floor": upper_floor,
        "Floors": lower_floor,

        "Price": price_gel,
        "productPriceM2": round(float(price_gel) / float(match.group(1)), 1),

        "MapLat": lat,
        "MapLon": lng,
        "MapZoom": zoom,
        "Images[]": images,

        **{key: value for amenity in mapped_amenities_first for key, value in amenity.items()},
        **{key: value for amenity in mapped_amenities_second for key, value in amenity.items()},
        **{key: value for keyword in keyword_objects for key, value in keyword.items()},

        "is_already_listed": False,
        "ProductTypeID": "1",
        "loc_city": "1",

        "loc_city_title_ka": "თბილისი",
        "loc_city_title_en": "თბილისი",
        "loc_city_title_ru": "თბილისი",

        "loc_city_seo_title_ka": "თბილისში",
        "loc_city_seo_title_en": "თბილისში",
        "loc_city_seo_title_ru": "თბილისში",

        "listing_id":listing_id,

        "IsDev": "0",
        "Phone": phone_number,
        "phoneIsActive": "1",
        "PromBlockAutoUpdateHour": "0",
        "PromBlockAutoUpdateQuantity": "1",
        "aupdate_packet": "0",
        "PromBlockColorQuantity": "0",
        "color_packet": "0",
        "vip_packet": "0",
        "StreetAddr": "",
        "loc_street": "1",
        "vip_plus_packet": "0",
        "PromBlockVipQuantity": "0",
        "CadCode": "",
        "super_vip_packet": "1",
        "ChangeInfo": "",
        "ProductOwner": "Tbilisi",
        "PaymentMethod": "balance",
        "PayWithCard": "0",
        "CurrencyID": "3",
        "UserEmail": email,
        "draftId": "6167953",
        "PrID": "",
        "Code": "",
        "IP": "87.253.53.94"

    }

    property_info.update(additional_data)

    # Return the information as JSON
    return json.loads(json.dumps(property_info))
