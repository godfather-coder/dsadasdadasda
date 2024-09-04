import time
import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction

from .convertDatas import TypeMapper
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
            mapper = TypeMapper()

            address = mapper.fetch_search_results(convertedData['ka[address]'], 'ka')
            print(address)
            utiles = Utiles()
            application_data1 = {
                "application": {
                    "userType":"Individual",
                    "realEstateTypeId":mapper.estate_type_id(convertedData['real_estate_type_id']),
                    "realEstateDealTypeId":mapper.deal_type_id(convertedData['deal_type_id']),
                    "cityId":95,
                    "currencyId":convertedData['currency_id'],
                    "showSiteCurrencyId":convertedData['currency_id'],
                    "priceType":convertedData['price_type_id'],
                    "phoneNumbers":[
                        {
                            "hasViber":False,
                            "hasWhatsapp":False,
                            "isApproved":False,
                            "isMain":True,
                            "phoneNumber":convertedData['phone_number']
                        }
                    ],
                    "subdistrictId":address['subDistrictId'],
                    "streetId":address['streetId'],
                    "bedrooms":3,
                    "price":3230,
                    "priceUsd":1200,
                    "unitPrice":29,
                    "unitPriceUsd":11,
                    "balconyLoggia":412,
                    "status":2,
                    "viewOnTheYard":True,
                    "balcony":True,
                    "garage":False,
                    "naturalGas":True,
                    "storage":True,
                    "cadastralCode":"None",
                    "heating":True,
                    "basement":False,
                    "elevator":True,
                    "lastFloor":False,
                    "descriptionGe":"ბინა არის იდეალურ მდგომარეობაში უცხოვრებელი. ვარ მეპატრონე.\nშეზღუდვები მაქვს შინაურ ცხოველებზე,.",
                    "descriptionEn":"The apartment is in perfect condition, uninhabited. I am the owner. I have restrictions on pets.",
                    "descriptionRu":"Квартира в идеальном состоянии, нежилая. Я владелец. У меня есть ограничения на домашних животных.",
                    "cableTelevision":True,
                    "drinkingWater":False,
                    "electricity":False,
                    "fridge":True,
                    "furniture":True,
                    "glazedWindows":True,
                    "hotWater":True,
                    "internet":True,
                    "ironDoor":True,
                    "securityAlarm":False,
                    "sewage":False,
                    "telephone":False,
                    "tv":True,
                    "washingMachine":True,
                    "water":False,
                    "wiFi":False,
                    "withPool":False,
                    "viewOnTheStreet":True,
                    "comfortable":True,
                    "light":True,
                    "airConditioning":True,
                    "commercialRealEstateType":0,
                    "floorType":0,
                    "kitchenArea":"20",
                    "contactPerson":"პაპუნა",
                    "hasRemoteViewing":False,
                    "isForUkraine":False,
                    "isPetFriendly":False,
                    "project":26,
                    "state":16,
                    "rooms":"4",
                    "floor":convertedData['floor'],
                    "floors":convertedData['floors'],
                    "toilet":418,
                    "totalArea":convertedData['area']
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
            application_data1['application']['realEstateApplicationId'] = applicationIdDr['applicationId']

            api = PaidServiceAPI(sstoken)

            ssResponse = api.create_application(application_data1)


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
