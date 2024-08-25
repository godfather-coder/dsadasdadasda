import requests

# Define the URL
url = "https://api3.myhome.ge/api/ka/user/payments/pay"

# Define the payload
payload = {
    "action": "payProduct",
    "amount": 0.1,
    "pay_with_card": 0,
    "payment_method": "1",
    "pcount": 1,
    "pr_ids": [19064775],
    "return_url": "http://example.com",
    "pay_with": None,
    "user_card_id": None
}

# Define the headers
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8,ka;q=0.7",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ2IjoiMSIsImlhdCI6MTcyNDYwMDk1NSwiZXhwaXJlc19hdCI6MTcyNDYwMTYxNSwiZGF0YSI6eyJ1c2VyX2lkIjo1MzY0NTEzLCJ1c2VybmFtZSI6InRhcmllbGludmVzdEBnbWFpbC5jb20iLCJzZXNzaW9uX2lkIjoiZDYwZjMyMDZkMzUyYjA2NDc3MWU5NWIwYmM1MGUxYjMwODA0Y2MzOWU0ZTRlYjVkZjE5YTg3YTk5NWM5YzQ2ZTBiZjE4ZGY5NTdjNGM0MjNlY2NiNDZlMzc2ZjY2ZjA4NTVjZTM1ZGRlNjNmMzkxYWQwM2YyYjkxYmZjZTJmYmQiLCJsaXZvX3VzZXJfaWQiOjEwMTY4MDIxLCJ2ZW5kb29fdXNlcl9pZCI6bnVsbCwic3dvb3BfdXNlcl9pZCI6bnVsbCwiZ2VuZGVyX2lkIjoxLCJiaXJ0aF95ZWFyIjoxOTk4LCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6IjU5MTA4MjQ5MyIsInVzZXJfbmFtZSI6IlRhcmllbCIsInVzZXJfc3VybmFtZSI6IkludmVzdCIsInR5cGVfaWQiOjB9fQ.0ipwFTfxE3HMVwbfkCfcKtDjpMIlBhso7-eBcFOh3l-Crl11FupuQ-PXciTReYUFWhv9jvwEXLDKTOm3OU3zMUcryLSSVUG5-P59LHHVW3z7rcacCJEVoxrTleJkIeFu8lmXKHp8YwxCzozdnA2SUyPXlO9mqmX6QZsMozIPsWTQyg_71xRJvF5w1KunIf-VmXsiHuz4yO9_i0YklmzR5Tt6W-rlTz7FRU0Hw9MaunJ7TX_txHU56-fS4VDC1d5ykbYjLIAbSLhvEn_QdEdN1KCatlvQB22F-maQm7-dXim_2cXzGHUyjDC4jMiAfXYfip8gjttm1iLI_Bv8-tgsAg",
    "content-type": "application/json",
    "origin": "https://www.myhome.ge",
    "referer": "https://www.myhome.ge/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# Include the cookies from your browser session
cookies = {
    'cookie_name': 'cookie_value'  # Replace with actual cookie name and value
}

# Make the POST request with a session
session = requests.Session()
response = session.post(url, json=payload, headers=headers, cookies=cookies)

# Print the response
print(response.status_code)
print(response.text)
