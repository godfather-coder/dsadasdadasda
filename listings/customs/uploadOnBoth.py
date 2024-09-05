from .ss.PaidServiceAPI import PaidServiceAPI
from .ss.RealEstateDraftCreator import RealEstateClient
from .ss.deleteDraft import DeleteDraft
from .convertDatas import TypeMapper


def fromMyhomeToSS(convertedData, sstoken):
    mapper = TypeMapper()
    address = mapper.fetch_search_results(convertedData['ka[address]'], 'ka')
    application_data1 = {
        "application": {
            "userType": "Individual",
            "realEstateTypeId": mapper.estate_type_id(convertedData['real_estate_type_id']),
            "realEstateDealTypeId": mapper.deal_type_id(convertedData['deal_type_id']),
            "cityId": 95,
            "currencyId": convertedData['currency_id'],
            "showSiteCurrencyId": convertedData['currency_id'],
            "priceType": convertedData['price_type_id'],
            "phoneNumbers": [
                {
                    "hasViber": False,
                    "hasWhatsapp": False,
                    "isApproved": False,
                    "isMain": True,
                    "phoneNumber": convertedData['phone_number']
                }
            ],
            "bedrooms": convertedData['bedroom_type_id'],
            "price": convertedData['total_price'],
            "priceUsd": convertedData['total_price'],
            "unitPrice": convertedData['square_price'],
            # "unitPriceUsd":11,
            "balconyLoggia": 412,
            "status": 2,
            "viewOnTheYard": False,
            "balcony": False,
            "garage": False,
            "naturalGas": False,
            "storage": False,
            "cadastralCode": "None",
            "heating": False,
            "basement": False,
            "elevator": False,
            "lastFloor": False,
            "descriptionGe": convertedData['ka[comment]'],
            "descriptionEn": convertedData['en[comment]'],
            "descriptionRu": convertedData['ru[comment]'],
            "cableTelevision": False,
            "drinkingWater": False,
            "electricity": False,
            "fridge": False,
            "furniture": False,
            "glazedWindows": False,
            "hotWater": False,
            "internet": False,
            "ironDoor": False,
            "securityAlarm": False,
            "sewage": False,
            "telephone": False,
            "tv": False,
            "washingMachine": False,
            "water": False,
            "wiFi": False,
            "withPool": False,
            "viewOnTheStreet": False,
            "comfortable": False,
            "light": False,
            "airConditioning": False,
            "commercialRealEstateType": 0,
            # "kitchenArea":"20",
            "contactPerson": convertedData['ka[owner_name]'],
            "hasRemoteViewing": False,
            "isForUkraine": False,
            "isPetFriendly": False,
            "project": mapper.project_type_id(convertedData['project_type_id']),
            "state": 16,
            "rooms": convertedData['room_type_id'],
            "toilet": 418,
            "totalArea": convertedData['area'],
            "subDistrictId": address['subDistrictId'],
            "streetId": address['streetId'],
            "floor": convertedData['floor'],
            "floors": convertedData['total_floors'],

        },
    }

    print(application_data1)

    delte = DeleteDraft(sstoken)
    delte.delete_draft()
    api_client = RealEstateClient(sstoken)
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



    return ssResponse
