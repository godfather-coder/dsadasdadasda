def map_json_fields(data, from_website):

    # Mapping from ss to myhome
    ss_to_myhome_mapping = {
        "realEstateTypeId": "real_estate_type_id",
        "realEstateDealTypeId": "deal_type_id",
        "cityId": "city_id",
        "streetId": "street_id",
        "districtId": "district_id",
        "subdistrictId": "urban_id",
        "price": "total_price",
        "currencyId": "currency_id",
        "status": "status_id",
        "project": "project_type_id",
        "rooms": "room_type_id",
        "bedrooms": "bedroom_type_id",
        "toilet": "bathroom_type_id",
        "floors": "total_floors",
        "heating": "heating_type_id",
        "garage": "parking_type_id",
        "hotWater": "hot_water_type_id",
        "floor": "material_type_id",
        "state": "condition_id",
        "totalArea": "area",
        "priceType": "price_type_id",
        "unitPrice": "square_price",
        "phoneNumbers": "phone_number",
        "descriptionGe": "ka[comment]",
        "descriptionEn": "en[comment]",
        "descriptionRu": "ru[comment]",
        "streetNumber": "ka[address]",
        "contactPerson": "ka[owner_name]",

    }

    # Reverse mapping from myhome to ss
    myhome_to_ss_mapping = {v: k for k, v in ss_to_myhome_mapping.items()}

    # Choose the correct mapping based on the from_website
    if from_website == "ss":
        mapping = ss_to_myhome_mapping
    elif from_website == "myhome":
        mapping = myhome_to_ss_mapping
    else:
        raise ValueError("Invalid website name. Use 'ss' or 'myhome'.")

    converted_data = {}

    for key, value in data.items():
        new_key = mapping.get(key, key)  # Default to the original key if no mapping is found
        if isinstance(value, dict):
            # Recursively map nested dictionaries
            converted_data[new_key] = map_json_fields(value, from_website)
        elif isinstance(value, list):
            # Recursively map lists of dictionaries
            converted_data[new_key] = [
                map_json_fields(item, from_website) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            converted_data[new_key] = value

    return converted_data

data = {
    'real_estate_type_id': (None, '1'),
    'deal_type_id': (None, '7'),
    'city_id': (None, '1'),
    'street_id': (None, '2952'),
    'district_id': (None, '1'),
    'urban_id': (None, '2'),
    'appear_rs_code': (None, '0'),
    'longitude': (None, '44.809154'),
    'latitude': (None, '41.795282'),
    'duration_id': (None, '1'),
    'status_id': (None, '2'),
    'project_type_id': (None, '8'),
    'room_type_id': (None, '2'),
    'bedroom_type_id': (None, '1'),
    'bathroom_type_id': (None, '1'),
    'floor': (None, '16'),
    'total_floors': (None, '19'),
    'height': (None, '0'),
    'balconies': (None, '1'),
    'balcony_area': (None, '9'),
    'heating_type_id': (None, '1'),
    'parking_type_id': (None, '2'),
    'hot_water_type_id': (None, '6'),
    'condition_id': (None, '1'),
    'area': (None, '45'),
    'area_type_id': (None, '1'),
    'price_type_id': (None, '3'),
    'total_price': (None, '40'),
    'square_price': (None, '0'),
    'currency_id': (None, '1'),
    'phone_number': (None, '591082493'),
    'ka[comment]': (None, '🗣️ ქირავდება ბინები მეორედან მე 19 სართულის ჩათვლით. ღამე 40 ლ!!!! 13:00 17:00 საათებში კი სულ რაღაც 30 ლარი.<br />\nერთ საძინებლიანი ბინების ფასები 24 საათი 50,60, 70 ლარი, ხოლო 2 საძინებლიანის ფასები 24 საათი 80.90 ლარი <br />\n1 საძინებლიანის ფასი მოიცავს 2 ადამიანის ოთახში განთავსებას! 2 საძინებლიანში 4 ადამიანის განთავსებას!<br />\nსტუმრების კომფორტისათვის ეზოში და კორპუსის პირველ სართულზე მუშაობს სუპერ მარკეტები 24/7ზე.<br />\nსაპარკინგე სივრცე.<br />\nბინების დასაჯავშნად / For room reservations:<br />\n 597997499<br />\nან მოგვწერეთ.<br />\nგლდანი, ქერჩის 6 ვ(20ა)შაურმების შუქნიშანი'),
    'ka[address]': (None, 'ქერჩის ქ. '),
    'ka[owner_name]': (None, 'Tariel'),
    'en[comment]': (None, '🗣️ ქირავდება ბინები მეორედან მე 19 სართულის ჩათვლით. ღამე 40 ლ!!!! 13:00 17:00 საათებში კი სულ რაღაც 30 ლარი.<br />\nერთ საძინებლიანი ბინების ფასები 24 საათი 50,60, 70 ლარი, ხოლო 2 საძინებლიანის ფასები 24 საათი 80.90 ლარი <br />\n1 საძინებლიანის ფასი მოიცავს 2 ადამიანის ოთახში განთავსებას! 2 საძინებლიანში 4 ადამიანის განთავსებას!<br />\nსტუმრების კომფორტისათვის ეზოში და კორპუსის პირველ სართულზე მუშაობს სუპერ მარკეტები 24/7ზე.<br />\nსაპარკინგე სივრცე.<br />\nბინების დასაჯავშნად / For room reservations:<br />\n 597997499<br />\nან მოგვწერეთ.<br />\nგლდანი, ქერჩის 6 ვ(20ა)შაურმების შუქნიშანი'),
    'en[address]': (None, 'ქერჩის ქ. '),
    'en[owner_name]': (None, 'Tariel'),
    'ru[comment]': (None, '🗣️ ქირავდება ბინები მეორედან მე 19 სართულის ჩათვლით. ღამე 40 ლ!!!! 13:00 17:00 საათებში კი სულ რაღაც 30 ლარი.<br />\nერთ საძინებლიანი ბინების ფასები 24 საათი 50,60, 70 ლარი, ხოლო 2 საძინებლიანის ფასები 24 საათი 80.90 ლარი <br />\n1 საძინებლიანის ფასი მოიცავს 2 ადამიანის ოთახში განთავსებას! 2 საძინებლიანში 4 ადამიანის განთავსებას!<br />\nსტუმრების კომფორტისათვის ეზოში და კორპუსის პირველ სართულზე მუშაობს სუპერ მარკეტები 24/7ზე.<br />\nსაპარკინგე სივრცე.<br />\nბინების დასაჯავშნად / For room reservations:<br />\n 597997499<br />\nან მოგვწერეთ.<br />\nგლდანი, ქერჩის 6 ვ(20ა)შაურმების შუქნიშანი'),
    'ru[address]': (None, 'ქერჩის ქ. '),
    'ru[owner_name]': (None, 'Tariel'),
    'parameters[0]': (None, '2'),
    'parameters[1]': (None, '3'),
    'parameters[2]': (None, '1'),
    'parameters[3]': (None, '10'),
    'parameters[4]': (None, '6'),
    'parameters[5]': (None, '8'),
    'parameters[6]': (None, '43'),
    'parameters[7]': (None, '44'),
    'parameters[8]': (None, '45'),
    'parameters[9]': (None, '46'),
    'parameters[10]': (None, '19'),
    'parameters[11]': (None, '23'),
    'parameters[12]': (None, '24'),
    'parameters[13]': (None, '26'),
    'parameters[14]': (None, '36'),
    'parameters[15]': (None, '4'),
    'parameters[16]': (None, '16'),
    'parameters[17]': (None, '17'),
    'parameters[18]': (None, '47'),
    'websites[0]': (None, '2')
}


print(map_json_fields(data, "myhome"))