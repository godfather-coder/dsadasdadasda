import requests


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

    def create_draft(self,data):
        url = f"{self.base_url}/v1/RealEstate/create-draft"

        response = requests.post(url, headers=self.headers, json=data)
        print("$$$$$$$$")
        print(response.json())

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


# # Example usage
# if __name__ == "__main__":
#     token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkEzMTIxOUJCRUNCNTkyNkNEOTEzMzJDMkIwNTMzMEJERENFNkRBODJSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im94SVp1LXkxa216WkV6TENzRk13dmR6bTJvSSJ9.eyJuYmYiOjE3MjQzMTQ3ODUsImV4cCI6MTcyNDMxODM4NSwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnNzLmdlIiwiYXVkIjpbInVzZXJfcmVnaXN0cmF0aW9uIiwiSm9iYXJpYUFQSSIsInBhaWRfc2VydmljZXMiLCJ3ZWJfYXBpZ2F0ZXdheSIsInJlYWxfZXN0YXRlIiwic3RhdGlzdGljcyIsImZpbGVzIiwiaG91c2VfYXBpIl0sImNsaWVudF9pZCI6InNzd2ViIiwic3ViIjoiYWE2NDE0NjUtNDk3OS00ZGJjLTgwY2YtMWM1NTMxOTZhODIzIiwiYXV0aF90aW1lIjoxNzIzOTA0MjA4LCJpZHAiOiJsb2NhbCIsInByZWZlcnJlZF91c2VybmFtZSI6IjU3NzQxNzA0NyIsIklzUHJlbWl1bSI6IkZhbHNlIiwiU2hvd0FkcyI6IlRydWUiLCJwaG9uZV9udW1iZXIiOiI1Nzc0MTcwNDciLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOiJUcnVlIiwiVXNlckVudGl0eVR5cGUiOiJJbmRpdmlkdWFsIiwiUElOIjoiOTUzNTQzNSIsIm5hbWUiOiJzYWRucmluaW8iLCJSb2xlcyI6IiIsImlhdCI6MTcyNDMxNDc4NSwic2NvcGUiOlsiZmlsZXMiLCJob3VzZV9hcGkiLCJvcGVuaWQiLCJwYWlkX3NlcnZpY2VzIiwicHJvZmlsZSIsInJlYWxfZXN0YXRlIiwic3RhdGlzdGljcyIsInVzZXJfcmVnaXN0cmF0aW9uIiwid2ViX2FwaWdhdGV3YXkiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl19.NXCNYCQpHgsn4Em9k8Mk22FmDa0AHxK77wulZ2dtZ_ygSQybyKixUtzwhXB7WPMMGqBq1NYXcGsSMne9pqFCHTyLTwbUYsloKCn7hdz4luNYouZu46tK9sn12GQCxBFf3tUD3etzTaOQnCCi-RkC4YDiRkEbR6zezisvJCLIuecViT_x-yN0a3GunzNNl70nSZvj4i8wZU_6_jpLV5_ozHMCRzsMoimwjgNfIEOfHrsyDlyvI-MfYLhK3onXkZGhEQEM_GtglKzSECgPOTtiQlrMqglw61TAtyr9-X-nnkOuixs3Kft1bzoU6OOssUbaEEGpZb0mDUVnRgOjKSOuWQ"
#     client = RealEstateClient(token)
#
#
#     try:
#         draft_response = client.create_draft()
#         print(draft_response)
#     except requests.exceptions.HTTPError as err:
#         print(f"HTTP error occurred: {err}")
#     except Exception as err:
#         print(f"Other error occurred: {err}")
