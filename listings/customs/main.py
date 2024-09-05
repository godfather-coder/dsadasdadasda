
import base64
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from .getListingData import UrlFetcher
from .formatData import FormatData
from .uploadListing import AddListing
from .uploadOnBoth import fromMyhomeToSS


def upload(ids, token, user, sstoken):
    result = []
    successful_uploads = 0
    failed_uploads = []

    def process_single_id(singleId):
        try:
            header, payload, signature = token.split(".")

            decoded_payload = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4))
            decoded_payload_json = json.loads(decoded_payload)

            test = UrlFetcher()
            data = test.fetch_data(singleId)

            convert = FormatData()
            convertedData = convert.convert_to_upload_format(
                data, decoded_payload_json.get('data').get('phone'),
                decoded_payload_json.get('data').get('user_name')
            )

            uploader = AddListing()
            uploader.setHeaders(token)

            response2 = None
            response = uploader.data(convertedData)
            if sstoken:
                response2 = fromMyhomeToSS(convertedData, sstoken)

            if response == 200 and response2 == 200 and sstoken:
                return "განცხადება " + singleId + " ორივე საიტზე წარმატებით დაიდო", singleId, True
            elif response !=200 and response2 == 200 and sstoken:
                return "განცხადება " + singleId + " ვერ დაიდო მაიჰოუმზე, მაგრამ დაიდო სსზე", singleId, False
            elif response == 200 and response2 != 200 and sstoken:
                return "განცხადება " + singleId + " ვერ დაიდო სსზე, მაგრამ დაიდო მაიჰოუმზე", singleId, False
            elif response ==200 and not sstoken:
                return "განცხადება " + singleId + " წარმატებით დაიდო მაიჰოუმზე", singleId, False
            else:
                return "შეცდომა აიდი " + singleId + "-ის დადებისას", singleId, False
        except Exception as e:
            print(e)
            return "შეცდომა აიდი " + singleId + "-ის დადებისას", singleId, False

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(process_single_id, singleId): singleId for singleId in ids}

        for future in as_completed(future_to_id):
            message, singleId, success = future.result()
            result.append(message)
            if success:
                successful_uploads += 1
            else:
                failed_uploads.append(singleId)

    with transaction.atomic():
        user.total_listings += successful_uploads
        user.failed_listings_myhome.extend(failed_uploads)
        user.save()

    return result
