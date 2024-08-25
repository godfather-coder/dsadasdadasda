import requests

class DeleteDraft:
    def __init__(self, token):
        self.base_url = "https://api-gateway.ss.ge/v1/RealEstate/"
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

    def delete_draft(self, body=None):
        url = self.base_url + "delete-draft"
        if body is None:
            body = {}
        response = requests.delete(url, headers=self.headers, json=body)
        return response

# Usage example:

# # Replace with your actual token
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkEzMTIxOUJCRUNCNTkyNkNEOTEzMzJDMkIwNTMzMEJERENFNkRBODJSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im94SVp1LXkxa216WkV6TENzRk13dmR6bTJvSSJ9.eyJuYmYiOjE3MjQzMjQzMTMsImV4cCI6MTcyNDMyNzkxMywiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnNzLmdlIiwiYXVkIjpbInVzZXJfcmVnaXN0cmF0aW9uIiwiSm9iYXJpYUFQSSIsInBhaWRfc2VydmljZXMiLCJ3ZWJfYXBpZ2F0ZXdheSIsInJlYWxfZXN0YXRlIiwic3RhdGlzdGljcyIsImZpbGVzIiwiaG91c2VfYXBpIl0sImNsaWVudF9pZCI6InNzd2ViIiwic3ViIjoiYWE2NDE0NjUtNDk3OS00ZGJjLTgwY2YtMWM1NTMxOTZhODIzIiwiYXV0aF90aW1lIjoxNzIzOTA0MjA4LCJpZHAiOiJsb2NhbCIsInByZWZlcnJlZF91c2VybmFtZSI6IjU3NzQxNzA0NyIsIklzUHJlbWl1bSI6IkZhbHNlIiwiU2hvd0FkcyI6IlRydWUiLCJwaG9uZV9udW1iZXIiOiI1Nzc0MTcwNDciLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOiJUcnVlIiwiVXNlckVudGl0eVR5cGUiOiJJbmRpdmlkdWFsIiwiUElOIjoiOTUzNTQzNSIsIm5hbWUiOiJzYWRucmluaW8iLCJSb2xlcyI6IiIsImlhdCI6MTcyNDMyNDMxMywic2NvcGUiOlsiZmlsZXMiLCJob3VzZV9hcGkiLCJvcGVuaWQiLCJwYWlkX3NlcnZpY2VzIiwicHJvZmlsZSIsInJlYWxfZXN0YXRlIiwic3RhdGlzdGljcyIsInVzZXJfcmVnaXN0cmF0aW9uIiwid2ViX2FwaWdhdGV3YXkiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl19.D_oEyi-_qssbWhP6tdWDIaCjqtnPfRV92AbFJgST_oWbUtnnV86QRaUyVvM71ZdyF8pa6nZBV8eEJjK-2rD2t5yDiJ2TBJq34CzX5YD_vFtwB6Xgk_jLFz_EiSJxLS-l7IRp56Fe8yb4TehCspTIoVhZos1Uk32WHq7SrJ-daaRmbS4PVJ-AGRUjW9MA0u0qRP52Uv6ZBlLOCBxVhrClDSYQMV1uoTFGhX_okA__oejsVkYUDDIB7jcSeEDoYxFLOlTs40N2djESErOhvBKz54cx8Nqs6YscNkrOVccN0jzt8ChqCJvU1tCmst2dxxa6eNYuEwhJ4osoNGz0kXT-ew"
#
# api = RealEstateAPI(token)
# response = api.delete_draft()

