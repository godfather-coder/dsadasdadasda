import requests
import json

from listings.customs.logCreator import log_user_action


class PaidServiceAPI:
    def __init__(self, auth_token):
        self.base_url = "https://api-gateway.ss.ge"
        self.auth_token = auth_token
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ka",
            "Authorization": f"Bearer {self.auth_token}",
            "content-type": "application/json",
            "origin": "https://home.ss.ge",
            "referer": "https://home.ss.ge/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/127.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

    def create_application(self, application_data,user, session_id):
        url = f"{self.base_url}/v1/PaidService/create-application"
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=application_data
            )


            print(response.status_code)
            log_user_action(user, 'სს-ის დადების რესპონსი',
                            details=f'სტატუს კოდი: {response.status_code}, დატა: {response.json()}', session_id=session_id)
            response.raise_for_status()  # Raise an exception for HTTP error responses
            try:
                return response.status_code
            except json.JSONDecodeError:
                return "შეცდომა"

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None