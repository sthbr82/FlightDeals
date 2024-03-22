import os

import requests
from datetime import datetime, timedelta

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.headers = {
            "apikey": os.environ["TEQUILA_API_KEY"]
        }

    def get_destination_iata_code(self, query):
        params = {
            "term": query['city'],
            "location_types": "city",
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=self.headers, params=params)
        airport_data_json = response.json()
        return airport_data_json['locations'][0]["code"]

    def get_destination_price(self, city_iata_code, fd_obj):
        date_from = datetime.now() + timedelta(days=1)
        date_to = datetime.now() + timedelta(days=180)

        fd_obj.inbound_date = date_from.strftime("%d/%m/%Y")
        fd_obj.outbound_date = date_to.strftime("%d/%m/%Y")

        params = {
            "fly_from": fd_obj.origin_airport_code,
            "fly_to": city_iata_code,
            "date_from": fd_obj.inbound_date,
            "date_to": fd_obj.outbound_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "INR",
            "max_stopovers": fd_obj.stop_overs,
            "max_sector_stopovers": fd_obj.stop_overs,
            "limit": 200
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/search", headers=self.headers, params=params)
        destination_data_json = response.json()

        if destination_data_json['data']:
            if fd_obj.stop_overs == 1:
                if destination_data_json['data'][0]['route'][0]['flyTo'] == \
                        destination_data_json['data'][1]['route'][0]['flyFrom']:
                    fd_obj.via_city = destination_data_json = destination_data_json['data'][0]['route'][0]['flyTo']
                    return destination_data_json['data'][0]['cityTo'], destination_data_json['data'][0]['fare'][
                        'adults'], fd_obj.via_city
            else:
                return destination_data_json['data'][0]['cityTo'], destination_data_json['data'][0]['fare']['adults']
        else:
            return None, 0
