import requests
from bs4 import BeautifulSoup
import json


class WebDataExtractor:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_html(self):
        """Fetch the HTML content from the URL."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Check if the request was successful
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def extract_data_by_div_id(self, div_id):
        """Extract data from a div element with a specific id."""
        if not self.soup:
            print("HTML content is not fetched yet.")
            return None

        div_data = self.soup.find('script', id=div_id)
        if div_data:
            return div_data.text  # Return the text inside the div
        else:
            print(f"No div with id '{div_id}' found.")
            return None

    def extract_application_data(self, div_id):
        """Extract only the 'applicationData' from the JSON data within the specified div."""
        json_data = self.extract_data_by_div_id(div_id)

        if json_data:
            try:
                # Parse the JSON data
                data = json.loads(json_data)

                # Navigate to the 'applicationData' child
                application_data = data.get('props', {}).get('pageProps', {}).get('applicationData', None)

                if application_data:
                    return application_data
                else:
                    print("'applicationData' not found in the JSON.")
                    return None
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        return None


