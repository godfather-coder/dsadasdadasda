def map_payload(first_site_data):
    # Define a mapping between the two website's fields
    field_mapping = {
        "real_estate_type_id": "realEstateTypeId",
        "deal_type_id": "realEstateDealTypeId",
        "city_id": "cityId",
        "street_id": "streetId",
        "total_price": "price",
        "square_price": "unitPrice",
        "currency_id": "currencyId",
        "ka[comment]": "descriptionGe",
        "en[comment]": "descriptionEn",
        "ru[comment]": "descriptionRu",
        "floor": "floor",
        "total_floors": "floors",
        "balcony_area": "balconyLoggia",
        "living_room_area": "kitchenArea",
        "area": "totalArea",
        "bedroom_type_id": "bedrooms",
        "condition_id": "state",
        "heating_type_id": "heating",
        "hot_water_type_id": "hotWater",
        "ka[owner_name]":"contactPerson",
        "status_id": "status",
        "ka[address]": "streetNumber",
        "price_type_id":"priceType",
        "bathroom_type_id": "toilet",
        "room_type_id": "rooms",
        "project_type_id": "project",
        "urban_id": "subdistrictId",
        "district_id": "districtId",

        # Add more mappings as needed
    }

    # Create the payload for the second website
    second_site_payload = {}

    for key, value in first_site_data.items():
        if key in field_mapping:
            second_site_payload[field_mapping[key]] = value
        elif key.startswith("parameters["):
            # Example handling for array parameters
            param_index = int(key.replace("parameters[", "").replace("]", ""))
            second_site_payload.setdefault("parameters", [])[param_index] = value

    # Handle boolean fields explicitly
    boolean_fields = [
        "hasRemoteViewing", "isForUkraine", "isPetFriendly", "airConditioning",
        "balcony", "basement", "cableTelevision", "drinkingWater", "electricity",
        "elevator", "fridge", "furniture", "garage", "glazedWindows", "heating",
        "hotWater", "internet", "ironDoor", "lastFloor", "naturalGas", "securityAlarm",
        "sewage", "storage", "telephone", "tv", "washingMachine", "water", "wiFi",
        "withPool", "viewOnTheYard", "viewOnTheStreet", "comfortable", "light"
    ]

    for field in boolean_fields:
        second_site_payload[field] = False  # Default to False or adjust logic as needed

    return second_site_payload


# Example usage with the first website's data:
first_site_data = {
    "real_estate_type_id": "1",
    "deal_type_id": "1",
    "city_id": "1",
    "street_id": "3138",
    "district_id": "4",
    "urban_id": "47",
    "rs_code": "",
    "appear_rs_code": "1",
    "longitude": "44.754554",
    "latitude": "41.725072",
    "duration_id": "1",
    "status_id": "1",
    "build_year_id": "1",
    "project_type_id": "3",
    "room_type_id": "5",
    "bedroom_type_id": "3",
    "bathroom_type_id": "2",
    "floor": "2",
    "total_floors": "22",
    "height": "2",
    "balconies": "1",
    "balcony_area": "10",
    "heating_type_id": "2",
    "parking_type_id": "4",
    "hot_water_type_id": "4",
    "material_type_id": "4",
    "condition_id": "3",
    "living_room_area": "22",
    "loggia_area": "11",
    "porch_area": "11",
    "storeroom_area": "11",
    "swimming_pool_type_id": "1",
    "living_room_type_id": "3",
    "storeroom_type_id": "9",
    "area": "222",
    "area_type_id": "1",
    "price_type_id": "3",
    "total_price": "1111",
    "square_price": "5",
    "currency_id": "1",
    "can_exchanged": "0",
    "hidden_owner_name": "Tbilisi",
    "hidden_owner_phone_number": "598757596",
    "hidden_owner_comment": "qwfwqwffwqwf",
    "ka[comment]":"wefgwef",
    "ka[address]":"ალექსანდრე ყაზბეგის გამზირი",
    "ka[owner_name]": "papuna",
    'ka[street_number]': "22",
    "en[comment]":"ewffefwe",
    "en[address]":"ალექსანდრე ყაზბეგის გამზირი",
    "en[owner_name]": "Kutaisi",
    "en[street_number]": "",
    "ru[comment]": "qwfqfqfqwf",
    "ru[address]": "ალექსანდრე ყაზბეგის გამზირი",
    "ru[owner_name]": "Kutaisi"




}

second_site_payload = map_payload(first_site_data)
print(second_site_payload)
