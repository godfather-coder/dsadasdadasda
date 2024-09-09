# main_file.py
import requests
from .mappings import estate_mapping, state_mapping, status_mapping, deal_mapping,project_type_mapping, attribute_id_mapping, urban_mapping, street_mapping

class TypeMapper:
    def __init__(self):
        # Initialize the mappings from the imported file
        self.estate_mapping = estate_mapping
        self.state_mapping = state_mapping
        self.status_mapping = status_mapping
        self.deal_mapping = deal_mapping
        self.project_type_mapping = project_type_mapping
        self.attribute_id_mapping = attribute_id_mapping
        self.urban_mapping = urban_mapping
        self.street_mapping = street_mapping

    def attr_id(self, attr):
        return self.attribute_id_mapping.get(attr, None)

    def street_id(self, number):
        # Return the mapped value for estate type or None if not found
        return self.street_mapping.get(str(number), None)

    def estate_type_id(self, number):
        return self.estate_mapping.get(number, None)

    def urban_id(self, number):
        return self.urban_mapping.get(number, None)

    def state(self, number):
        return self.state_mapping.get(number, 2)

    def status(self, number):
        return self.status_mapping.get(number, None)

    def deal_type_id(self, number):
        return self.deal_mapping.get(number, None)

    def project_type_id(self, number):
        return self.project_type_mapping.get(number, 4)

    # You can add the remaining methods here...

    def fetch_search_results(self, search, lang, urbanId):

        url = "https://home.ss.ge/api/search-loc"
        params = {'lang': lang}

        def fetch_data(search_param):
            """Fetch data from API based on the search parameter."""
            try:
                params['search'] = search_param
                response = requests.get(url, params=params)
                response.raise_for_status()
                print(response.status_code)
                return response.json()  # Get the JSON response
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for '{search_param}': {e}")
                return []

        # Split the search parameter by spaces and take the longest word
        words = search.split()
        longest_word = max(words, key=len) if words else ""

        # Create a list to collect results
        new = []

        # Fetch data using the longest word and add to results
        for word in [longest_word, longest_word[:-1], longest_word[:-2]]:
            print(word)
            data = fetch_data(word)
            for item in data:
                if item.get('cityId') == 95 and item not in new:
                    new.append(item)

        # Filter the results based on urbanId and return them
        filtered = [item for item in new if item.get('subDistrictId') == urbanId]

        return filtered[0]['streetId'] if filtered else {"message": "No matches found for the given urbanId."}


# Example usage:
# mapper = TypeMapper()
# search_result = mapper.fetch_search_results('საკანდელიძე ზ. ქ.', 'en', mapper.urban_id(28))
# print(search_result)
#
#
# print(mapper.urban_id(28))