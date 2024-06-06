from .getListingData import UrlFetcher
from .formatData import FormatData
from .uploadListing import AddListing
import base64
import json


token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ2IjoiMSIsImlhdCI6MTcxNzUyNTk1NCwiZXhwaXJlc19hdCI6MTcxNzUyNjYxNCwiZGF0YSI6eyJ1c2VyX2lkIjo1MzY0NTEzLCJ1c2VybmFtZSI6InRhcmllbGludmVzdEBnbWFpbC5jb20iLCJzZXNzaW9uX2lkIjoiM2ZhN2Y1YzIxZGU0NmJkMmU3NzY0ZGU3ODA4YjgwNGNiNjNlZjIyMDQzZmYwNWZlODM4NjAyZmUzYjRmNmY2MmFmY2UyY2EzNmQ4ZjgyNWNkZWFkM2E1MDhjZGQ4YTI1MTliNmVlYzI2NmY4MWY0MzVmYTUzM2FmMGRiYzI4ZGMiLCJsaXZvX3VzZXJfaWQiOjEwMTY4MDIxLCJ2ZW5kb29fdXNlcl9pZCI6bnVsbCwic3dvb3BfdXNlcl9pZCI6bnVsbCwiZ2VuZGVyX2lkIjoxLCJiaXJ0aF95ZWFyIjoxOTk4LCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6IjU5MTA4MjQ5MyIsInVzZXJfbmFtZSI6IlRhcmllbCIsInVzZXJfc3VybmFtZSI6IkludmVzdCIsInR5cGVfaWQiOjB9fQ.r3UflsADC-O9hHSAS3TQkui-aznVRWcW7vf9nFU4BvAOoDtkxJrpv8cuCRo4G6zev7diqb-whCkpAWhuRoG22oWxdvdVsn-dpRDrIdTaEZQV4Rlt9CEHYSFe1V4w6jnWhYE6U4uaKvM5BxJNCmHO5v40zzsQnFpKyvIUAQekntdzjFWehEhqOQBEZp0ipENtZCecowOGNFY9JnD5qXOP1tndRMjBWS8_kWuIwppYhPn5OMeNmR88RKLcqFgnYG0SihjdxMKJvaas-2k0CDNhMrVk05huTJwx7HIrhfkdXs2DpbGWy4t4xgvI9GH8jen-gZCOi6VnhI2WD3Cd_UVLFQ"

header, payload, signature = token.split(".")

decoded_payload = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4))
decoded_payload_json = json.loads(decoded_payload)

print(decoded_payload_json.get('data').get('phone'))
print(decoded_payload_json.get('data').get('user_name'))


test = UrlFetcher()

data = test.fetch_data(18266826)

convert = FormatData()

convertedData = convert.convert_to_upload_format(
    data, decoded_payload_json.get('data').get('phone')
    , decoded_payload_json.get('data').get('user_name')
)

uploader = AddListing()


uploader.setHeaders(token)
print(uploader.data(convertedData))
