import json

from .ss.ImageConverter import ImageConverter
from .ss.PaidServiceAPI import PaidServiceAPI
from .ss.RealEstateDraftCreator import RealEstateClient
from .ss.deleteDraft import DeleteDraft
from .convertDatas import TypeMapper
from .ss.main import uploadImagesSS
from .ss.ssImage import ImageUploader


def fromMyhomeToSS(convertedData, sstoken, image_urls):
    try:

        mapper = TypeMapper()
        print(convertedData['ka[address]'])
        print(mapper.street_id(convertedData['street_id']))
        print(mapper.fetch_search_results(convertedData['ka[address]'], 'ka', mapper.urban_id(convertedData['urban_id'])))
        if mapper.street_id(convertedData['street_id']) is None:
            street = mapper.street_id(convertedData['street_id'])
        else:
            street = mapper.fetch_search_results(convertedData['ka[address]'], 'ka', convertedData['urban_id'])



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
                "price": convertedData['total_price'],
                "priceUsd": convertedData['total_price'],
                "unitPrice": convertedData['square_price'],
                "unitPriceUsd": 11,
                "balconyLoggia": 412,
                "status": mapper.status(convertedData["status_id"]),
                # "airConditioning": mapper.attribute_id_mapping(),
                "hasRemoteViewing": False,
                "isForUkraine": False,
                "isPetFriendly": False,
                "cadastralCode": "None",

                "descriptionGe": convertedData['ka[comment]'],
                "descriptionEn": convertedData['en[comment]'],
                "descriptionRu": convertedData['ru[comment]'],

                "commercialRealEstateType": 0,
                # "kitchenArea": "20",
                "contactPerson": convertedData['ka[owner_name]'],

                "project": mapper.project_type_id(convertedData['project_type_id']),
                "state": mapper.state(convertedData['condition_id']),
                "rooms": convertedData['room_type_id'],

                "totalArea": convertedData['area'],
                # "subDistrictId": mapper.urban_id(convertedData['urban_id']),
                "streetId": street,
                "floor": convertedData['floor'],
                "floors": convertedData['total_floors'],
            },
        }

        if convertedData['bedroom_type_id'] is None or convertedData['bedroom_type_id'] == "None":
            application_data1['application']['bedrooms'] = 0
        else:
            application_data1['application']['bedrooms'] = convertedData['bedroom_type_id']

        if convertedData['bathroom_type_id'] is None or convertedData['bathroom_type_id'] == "None":
            application_data1['application']['toilet'] = 1
        else:
            application_data1['application']['toilet'] = convertedData['bathroom_type_id']

        delte = DeleteDraft(sstoken)
        delte.delete_draft()

        def extract_parameters(data):
            parameters = {}
            for key, value in data.items():
                if key.startswith("parameters"):
                    parameters[key] = value
            return parameters

        parameters = extract_parameters(convertedData)

        for key, value in parameters.items():
            attr_string = mapper.attr_id(value)
            if attr_string:
                new_element = '{' + attr_string + '}'

                new_element_dict = json.loads(new_element)

                application_data1['application'].update(new_element_dict)

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
        images = uploadImagesSS(image_urls, sstoken, applicationIdDr['applicationId'])

        application_data1['application']["images"] = images

        application_data1['application']['realEstateApplicationId'] = applicationIdDr['applicationId']

        api = PaidServiceAPI(sstoken)
        ssResponse = api.create_application(application_data1)
        return ssResponse
    except Exception as e:
        print(e)
        return "შეცდომა სს-ზე დადებისას"
