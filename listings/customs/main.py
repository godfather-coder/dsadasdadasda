import time
import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from .getListingData import UrlFetcher
from .formatData import FormatData
from .ss.PaidServiceAPI import PaidServiceAPI
from .ss.RealEstateDraftCreator import RealEstateClient
from .ss.deleteDraft import DeleteDraft
from .ss.utiles import Utiles
from .uploadListing import AddListing


def upload(ids, token, user, sstoken):
    result = []
    successful_uploads = 0
    failed_uploads = []

    def process_single_id(singleId):
        try:
            header, payload, signature = token.split(".")

            decoded_payload = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4))
            decoded_payload_json = json.loads(decoded_payload)

            test = UrlFetcher()
            data = test.fetch_data(singleId)

            convert = FormatData()
            convertedData = convert.convert_to_upload_format(
                data, decoded_payload_json.get('data').get('phone'),
                decoded_payload_json.get('data').get('user_name')
            )

            uploader = AddListing()
            uploader.setHeaders(token)

            utiles = Utiles()
            application_data1 = {
                "application": {
                    "userType": "Individual",
                    "realEstateTypeId": 3,
                    "realEstateDealTypeId": 4,
                    "cityId": 80,
                    "currencyId": 2,
                    "showSiteCurrencyId": 2,
                    "priceType": 1,
                    "phoneNumbers": [
                        {
                            "hasViber": False,
                            "hasWhatsapp": False,
                            "isApproved": False,
                            "isMain": True,
                            "phoneNumber": "598757596"
                        }
                    ],
                    "subdistrictId": "None",
                    "streetId": "None",
                    "bedrooms": 0,
                    "price": 593000,
                    "priceUsd": 220000,
                    "unitPrice": 121,
                    "unitPriceUsd": 45,
                    "balconyLoggia": 417,
                    "status": 0,
                    "viewOnTheYard": False,
                    "balcony": False,
                    "garage": False,
                    "naturalGas": True,
                    "storage": False,
                    "cadastralCode": "71.56.31.1456,71.56.31.1457,71.56.31.1458,71.56.31.1166,71.56.31.1167,71.56.31.1168,71.56.31.1463,71.56.31.415",
                    "heating": "False",
                     "basement":False,
                    "elevator": False,
                    "lastFloor": False,
                    "descriptionGe": "qwf ",
                    "descriptionEn": "qwffw",
                    "descriptionRu": "qwf",
                    "cableTelevision": False,
                    "drinkingWater": False,
                    "electricity": "True",
                    "fridge": False,
                    "furniture": False,
                    "glazedWindows": False,
                    "hotWater": False,
                    "internet": False,
                    "ironDoor": False,
                    "securityAlarm": False,
                    "sewage": True,
                    "telephone": False,
                    "tv": False,
                    "washingMachine": False,
                    "water": True,
                    "wiFi": False,
                    "withPool": False,
                    "viewOnTheStreet": False,
                    "comfortable": False,
                    "light": False,
                    "airConditioning": False,
                    "commercialRealEstateType": 0,
                    "floorType": 0,
                    "kitchenArea": "None",
                    "contactPerson": "პაპუნა",
                    "hasRemoteViewing": True,
                    "isForUkraine": False,
                    "isPetFriendly": False,
                    "streetNumber": "None",
                    "totalArea": 4900
                },
            }

            delte = DeleteDraft(sstoken)
            delte.delete_draft()
            api_client = RealEstateClient(sstoken)
            # response = uploader.data(convertedData)
            applicationIdDr = api_client.create_draft(application_data1['application'])
            application_data1['paidServices'] = {
                "isCreate": True,
                "items": [
                    {
                        "applicationId": applicationIdDr['applicationId'],
                        "rubric": "RealEstate",
                        "realEstateDealTypeId": 4,
                        "cityId": 95,
                        "paidServices": []
                    }
                ]
            }

            api = PaidServiceAPI(sstoken)

            # ssResponse = api.create_application(application_data1)
            #
            # print(ssResponse)

            print(applicationIdDr)

            if 200 == 200:
                print("აიტვირთა")
                return "განცხადება " + singleId + " წარმატებით დაიდო", singleId, True
            else:
                return "შეცდომა აიდი " + singleId + "-ის დადებისას", singleId, False
        except Exception as e:
            print(e)
            return "შეცდომა აიდი " + singleId + "-ის დადებისას", singleId, False

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(process_single_id, singleId): singleId for singleId in ids}

        for future in as_completed(future_to_id):
            message, singleId, success = future.result()
            result.append(message)
            if success:
                successful_uploads += 1
            else:
                failed_uploads.append(singleId)

    with transaction.atomic():
        user.total_listings += successful_uploads
        user.failed_listings_myhome.extend(failed_uploads)
        user.save()

    return result
