import base64
import json


class JWTExtractor:
    @staticmethod
    def base64_url_decode(input_str):
        input_str += '=' * (4 - len(input_str) % 4)
        return base64.urlsafe_b64decode(input_str)

    @staticmethod
    def extract_payload(token):
        try:
            header, payload, signature = token.split('.')
            decoded_payload = JWTExtractor.base64_url_decode(payload)
            payload_data = json.loads(decoded_payload.decode('utf-8'))
            return payload_data
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Error decoding token: {e}")
            return None


# Example usage
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkEzMTIxOUJCRUNCNTkyNkNEOTEzMzJDMkIwNTMzMEJERENFNkRBODJSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im94SVp1LXkxa216WkV6TENzRk13dmR6bTJvSSJ9.eyJuYmYiOjE3MjQ0NDQ5NDEsImV4cCI6MTcyNDQ0ODU0MSwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnNzLmdlIiwiYXVkIjpbInVzZXJfcmVnaXN0cmF0aW9uIiwiSm9iYXJpYUFQSSIsInBhaWRfc2VydmljZXMiLCJ3ZWJfYXBpZ2F0ZXdheSIsInJlYWxfZXN0YXRlIiwic3RhdGlzdGljcyIsImZpbGVzIiwiaG91c2VfYXBpIl0sImNsaWVudF9pZCI6InNzd2ViIiwic3ViIjoiYjRmYTY0YTYtMzAwNC00YTdkLWFmMjctZGU3YmNjOWE4N2E4IiwiYXV0aF90aW1lIjoxNzI0Mzk5OTY3LCJpZHAiOiJsb2NhbCIsInByZWZlcnJlZF91c2VybmFtZSI6IndwYXB1bmExOTk1QGdtYWlsLmNvbSIsIklzUHJlbWl1bSI6IkZhbHNlIiwiU2hvd0FkcyI6IlRydWUiLCJlbWFpbCI6IndwYXB1bmExOTk1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjoiVHJ1ZSIsInBob25lX251bWJlciI6IjU5ODc1NzU5NiIsInBob25lX251bWJlcl92ZXJpZmllZCI6IlRydWUiLCJVc2VyRW50aXR5VHlwZSI6IkluZGl2aWR1YWwiLCJQSU4iOiI5NTY0NDAwIiwibmFtZSI6IuGDnuGDkOGDnuGDo-GDnOGDkCIsIlJvbGVzIjoiIiwiaWF0IjoxNzI0NDQ0OTQxLCJzY29wZSI6WyJmaWxlcyIsImhvdXNlX2FwaSIsIm9wZW5pZCIsInBhaWRfc2VydmljZXMiLCJwcm9maWxlIiwicmVhbF9lc3RhdGUiLCJzdGF0aXN0aWNzIiwidXNlcl9yZWdpc3RyYXRpb24iLCJ3ZWJfYXBpZ2F0ZXdheSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJvdHAiXX0.FJsFZkxDq4hG9PD2SMAYTWE9Z2aTMZUdNzzLZY00Qtu28bFrJS6my09rpjsZakt7YfG0dF4EgTwDENrwB3IEBBiuWUfI8dbJ398OCLgeaYEmeF9POKDvicnbDdIy9b-huYbFfK2dtfyOSZ-Epvw42rxtSTo_48wozTRDNSMX6ZxY4WveuK7Kgh2cUFyyauE40x_UuHqcpk25JHN3jw9F1OXpbqgUbg4Yhsv7xgQ7RUysDxIqFy_ciIdElzFClRvvK5_NSTmv4jSDCCZzFYgEEg0-YhVF_ObUjh4TmIThXTXDNll6m0HVQaMPm-_gzlSyHrWsTLDWw5-_oZrtdLSIcA"
extractor = JWTExtractor()
payload_data = extractor.extract_payload(token)
print(payload_data['phone_number'])
print(payload_data['name'])