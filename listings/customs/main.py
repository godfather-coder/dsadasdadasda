import time

from .getListingData import UrlFetcher
from .formatData import FormatData
from .uploadListing import AddListing
import base64
import json


def upload(ids, token):
    for singleId in ids:
        header, payload, signature = token.split(".")

        decoded_payload = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4))
        decoded_payload_json = json.loads(decoded_payload)

        test = UrlFetcher()

        data = test.fetch_data(singleId)

        convert = FormatData()

        convertedData = convert.convert_to_upload_format(
            data, decoded_payload_json.get('data').get('phone')
            , decoded_payload_json.get('data').get('user_name')
        )

        uploader = AddListing()

        uploader.setHeaders(token)

        print(uploader.data(convertedData))
