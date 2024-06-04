import requests
from io import BytesIO


class AddListing:
    headers = {}

    def setHeaders(self, token):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "global-authorization": token,
            "locale": "ka",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://statements.tnet.ge/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

    def __init__(self):
        self.url = "https://api-statements.tnet.ge/v1/statements/create"

    def data(self, data1):
        data = {}
        if data1["deal_type_id"] ==1:
            data['can_exchanged'] = (None, 0)
        # if data1["deal_type_id"] != 7:
        #     data['build_year_id'] = (None, data1["build_year_id"])
        keys_to_check = [
            "real_estate_type_id", "deal_type_id", "city_id", "street_id", "district_id", "urban_id", "rs_code",
            "appear_rs_code", "longitude", "latitude", "duration_id", "status_id", "build_year_id", "project_type_id",
            "room_type_id", "bedroom_type_id", "bathroom_type_id", "floor", "total_floors", "height", "balconies",
            "balcony_area", "heating_type_id", "parking_type_id", "hot_water_type_id", "material_type_id",
            "condition_id", "living_room_area", "loggia_area", "porch_area", "storeroom_area", "swimming_pool_type_id",
            "living_room_type_id", "storeroom_type_id", "area", "area_type_id", "price_type_id", "total_price",
            "square_price", "currency_id", "phone_number", "ka[comment]", "ka[address]",
            "ka[owner_name]", "ka[street_number]", "en[comment]", "en[address]", "en[owner_name]", "ru[comment]",
            "ru[address]", "ru[owner_name]", "ru[street_number]"
        ]

        # Include mandatory fields
        for key in keys_to_check:
            value = data1.get(key)
            if value is not None:
                data[key] = (None, str(value))  # Convert value to string
        for i in data1.keys():
            if i.startswith("parameters"):
                data[i] = (None, str(data1[i]))
        # Add parameters to the data dictionary
        # parameters = [
        #     2, 3, 1, 6, 8, 24, 25, 47, 11, 26, 32, 34, 35, 9, 40, 13, 15, 5, 7, 12, 10, 43, 44, 45, 46, 19, 20, 4, 18,
        #     17, 16, 36, 51, 52, 55
        # ]
        # for i, param in enumerate(parameters):
        #     data[f"parameters[{i}]"] = (None, str(param))
        # Add websites
        data['websites[0]'] = (None, '2')

        images = []
        for key in data1.keys():
            if key.startswith("images["):
                images.append(data1[key])

        image_urls = [url for url in images if url]
        # data['deal_type_id'] = (None, '1')
        print(data1['deal_type_id'])
        for i, image_url in enumerate(image_urls):
            image_id, uploaded_url = self.upload_image(image_url)
            if image_id and uploaded_url:
                data[f"images[{i}][image_id]"] = (None, image_id)
                data[f"images[{i}][url]"] = (None, uploaded_url)
        print(data['deal_type_id'])
        print(str(data['status_id'])+"statusi")
        print(str(data1['status_id']) + "statusi data1Shi")
        # if 1 not in data['deal_type_id']:
        #     data['can_exchanged']=(None, 0)
        response = requests.post(self.url, headers=self.headers, files=data)
        print(response.json())

    def upload_image(self, image_url):
        try:
            # Step 1: Fetch the Image from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
            image_data = response.content

            # Step 2: Convert the Image into the Required Format
            image_file = BytesIO(image_data)
            image_file.name = "image.jpg"  # provide a filename for the file-like object

            # Step 3: Send the Image Data
            upload_url = "https://api-statements.tnet.ge/v1/statements/upload-image"

            files = {
                'image': (image_file.name, image_file, 'image/jpeg')  # adjust the content type if needed
            }

            response = requests.post(upload_url, headers=self.headers, files=files)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes

            uploaded_url = response.json()['data']['url']

            image_id = response.json()['data']['id']

            return image_id, uploaded_url

        except requests.exceptions.RequestException as e:
            # Handle exceptions like connection errors, timeouts, etc.
            print("Error:", e)
            return None, None