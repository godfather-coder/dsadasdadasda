import time

import requests
from io import BytesIO

from rest_framework.response import Response

from ..models import Listing


def upload_listing_for_sale(data, token, user):
    if Listing.objects.filter(listing_id=data.get("listing_id"), users=user).exists():
        return Response({"msg": "განცხადება ამ აიდით უკვე დევს"}, status=400)

    headers = {
        "accept": "application/json, text/javascript, /; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authtoken": token,
        "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://www.myhome.ge/ka/my/addProduct",
        "Referrer-Policy": "unsafe-url",
    }

    response = requests.post("https://api.myhome.ge/ka/Mypage/AddProduct", data=data, headers=headers)

    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        listing = Listing.objects.create(listing_id=data.get("listing_id"))
        listing.users.add(user)  # Associate the listing with the user
        return Response({"msg": "განცხადება აიტვირთა"}, status=200)
    else:
        print("Failed to upload listing.")
