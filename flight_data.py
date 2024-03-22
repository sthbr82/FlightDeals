import requests


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.price = 0
        self.destination_airport_code = ""
        self.destination_city = ""
        self.origin_city = ""
        self.origin_airport_code = ""
        self.inbound_data = ""
        self.outbound_date = ""
        self.stop_overs = 0
        self.via_city = ""


