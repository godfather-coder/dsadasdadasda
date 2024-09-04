import json

class FormatData:
    def __init__(self):
        pass

    def convert_to_upload_format(self, input_data, number,name):
        output_data = {}



        # Map simple fields
        statement = input_data['data']['statement']

        output_data['real_estate_type_id'] = statement.get('real_estate_type_id')
        output_data['deal_type_id'] = statement.get('deal_type_id')
        output_data['city_id'] = statement.get('city_id')
        output_data['street_id'] = statement.get('street_id', 496)  # Default value as an example
        output_data['district_id'] = statement.get('district_id')
        output_data['urban_id'] = statement.get('urban_id')
        output_data['longitude'] = statement.get('lng')
        output_data['latitude'] = statement.get('lat')
        output_data['total_price'] = statement.get('total_price')
        output_data['currency_id'] = statement.get('currency_id')

        # Default values for other required fields
        output_data['appear_rs_code'] = 0
        output_data['duration_id'] = 1
        output_data['status_id'] = statement.get('status_id')
        output_data['build_year_id'] = statement.get('build_year_id')
        output_data['project_type_id'] = statement.get('project_type_id')
        output_data['room_type_id'] = statement.get('room_type_id')
        output_data['bedroom_type_id'] = statement.get('bedroom_type_id')
        output_data['bathroom_type_id'] = statement.get('bathroom_type_id')
        output_data['floor'] = statement.get('floor')
        output_data['total_floors'] = statement.get('total_floors')
        output_data['height'] = statement.get('height')
        output_data['balconies'] = statement.get('balconies')
        output_data['balcony_area'] = statement.get('balcony_area', 5)  # Default value
        output_data['heating_type_id'] = statement.get('heating_type_id')
        output_data['parking_type_id'] = statement.get('parking_type_id')
        output_data['hot_water_type_id'] = statement.get('hot_water_type_id')
        output_data['material_type_id'] = statement.get('material_type_id')
        output_data['condition_id'] = statement.get('condition_id')
        output_data['living_room_area'] = statement.get('living_room_area', 10)  # Default value
        output_data['loggia_area'] = statement.get('loggia_area', 11)  # Default value
        output_data['porch_area'] = statement.get('porch_area', 11)  # Default value
        output_data['storeroom_area'] = statement.get('storeroom_area', 2)  # Default value
        output_data['swimming_pool_type_id'] = statement.get('swimming_pool_type_id')
        output_data['living_room_type_id'] = statement.get('living_room_type_id')
        output_data['storeroom_type_id'] = statement.get('storeroom_type_id')
        output_data['area'] = statement.get('area')
        output_data['area_type_id'] = 1
        output_data['price_type_id'] = 3
        output_data['square_price'] = statement.get('total_price') // statement.get('area')  # Example calculation
        output_data['can_exchanged'] = 0
        output_data['phone_number'] = number


        # Map parameters
        parameters = statement.get('parameters', [])
        for i, param in enumerate(parameters):
            output_data[f'parameters[{i}]'] = param['id']

        # Map multilingual fields
        output_data['ka[comment]'] = statement.get('comment')
        output_data['ka[address]'] = statement.get('address')
        output_data['ka[owner_name]'] = name
        output_data['en[comment]'] = statement.get('comment')
        output_data['en[address]'] = statement.get('address')
        output_data['en[owner_name]'] = name
        output_data['ru[comment]'] = statement.get('comment')
        output_data['ru[address]'] = statement.get('address')
        output_data['ru[owner_name]'] = name


        gallery = statement.get('gallery', [])
        for i, img in enumerate(gallery):
            output_data[f'images[{i}][image_id]'] = img['image'].get('id')
            output_data[f'images[{i}][url]'] = img['image'].get('large')

        # Convert dictionary to JSON
        return output_data
