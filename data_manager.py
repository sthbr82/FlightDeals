import requests
import os

SHEETY_ENDPOINT = "https://api.sheety.co"
API_KEY = os.environ["SHEETY_API_KEY"]


class DataManager:
    def __init__(self):
        BASIC_AUTH = f'Basic {os.environ["BASIC_AUTH"]}'
        BEARER_AUTH = f'Bearer {os.environ["BEARER_AUTH"]}'

        self.headers = {
            "Authorization": BEARER_AUTH
        }

    def get_flight_data(self):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/{API_KEY}/flightDeals/prices", headers=self.headers)
        return response

    def update_iata_code_in_sheet(self, sheet_data):
        update_params = {
            "price": {
                "iataCode": f"{sheet_data['iataCode']}"
            }
        }
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{API_KEY}/flightDeals/prices/{sheet_data['id']}",
                                json=update_params,  headers=self.headers)
        return response

