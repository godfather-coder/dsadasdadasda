import requests

class TypeMapper:
    def __init__(self):
        # Initialize the mappings as instance variables
        self.estate_mapping = {
            1: 5,
            2: 4,
            3: 1,
            4: 3,
            5: 6,
            6: 2,
        }
        self.deal_mapping = {
            1: 4,
            2: 1,
            3: 2,
            4: 3,
        }

    def estate_type_id(self, number):
        # Return the mapped value for estate type or None if not found
        return self.estate_mapping.get(number, None)

    def deal_type_id(self, number):
        # Return the mapped value for deal type or None if not found
        return self.deal_mapping.get(number, None)

    def fetch_search_results(self, search, lang):
        """
        Calls the API with the provided search and lang query parameters.

        Args:
            search (str): The search query parameter.
            lang (str): The language query parameter.

        Returns:
            dict: The JSON response from the API, or an error message if the request fails.
        """
        url = "https://home.ss.ge/api/search-loc"
        params = {'search': search, 'lang': lang}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()[0]  # Return the JSON response
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


# Example usage:
mapper = TypeMapper()
print(mapper.estate_type_id(1))  # Output: 5
print(mapper.deal_type_id(2))    # Output: 1

# Fetch search results with example parameters
search_result = mapper.fetch_search_results('ატენის ქ.', 'en')
print(search_result)
