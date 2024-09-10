import requests

from listings.customs.logCreator import log_user_action


class RealEstateClient:
    def __init__(self, token):
        self.base_url = "https://api-gateway.ss.ge"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ka",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "os": "web",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://home.ss.ge/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

    def create_draft(self,data, user, session_id):
        url = f"{self.base_url}/v1/RealEstate/create-draft"

        response = requests.post(url, headers=self.headers, json=data)
        print(response.status_code)
        log_user_action(user, 'სს-ის დრაფტის რესპონსი',
                        details=f'სტატუს კოდი: {response.status_code}, დატა: {response.json()}, Session ID: {session_id}', session_id=session_id)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()