import requests

class UrlFetcher:
    def __init__(self, headers=None, body=None, method='GET'):
        self.url = f"https://api-statements.tnet.ge/v1/statements/"
        self.headers = headers
        self.body = body
        self.method = method

        # Default headers if not provided
        if self.headers is None:
            self.headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "global-authorization": "",
                "locale": "ka",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "x-website-key": "myhome",
                "Referer": "https://www.myhome.ge/",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }

    def fetch_data(self,id):
        try:
            response = requests.request(self.method, self.url+str(id), headers=self.headers, data=self.body)
            if response.status_code == 200:
                return response.json()  # Assuming response is JSON
            else:
                return f"Error: Failed to fetch data from {self.url}. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"



