# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

if __name__ == "__main__":
    dm_obj = DataManager()
    fs_obj = FlightSearch()
    fd_obj = FlightData()
    nm_obj = NotificationManager()

    sheet_data = dm_obj.get_flight_data()
    json_data = sheet_data.json()
    sheet_data_prices = json_data["prices"]

    fd_obj.origin_airport_code = "BLR"
    fd_obj.origin_city = "Bengaluru"

    for destination in sheet_data_prices:
        fd_obj.stop_overs = 0
        if not destination['iataCode']:
            iata_code = fs_obj.get_destination_iata_code(destination)
            destination['iataCode'] = iata_code
            response = dm_obj.update_iata_code_in_sheet(destination)

        fd_obj.destination_city, fd_obj.price = fs_obj.get_destination_price(destination['iataCode'], fd_obj)
        fd_obj.destination_airport_code = destination['iataCode']

        if fd_obj.destination_city is None:
            fd_obj.stop_overs = 1
            fd_obj.destination_city, fd_obj.price = fs_obj.get_destination_price(destination['iataCode'], fd_obj)
            fd_obj.destination_airport_code = destination['iataCode']

        if fd_obj.destination_city is not None:
            print(f"{fd_obj.destination_city}: ₹{fd_obj.price}")
            if fd_obj.price < destination['lowestPrice']:
                nm_obj.send_sms_alert(fd_obj)
                nm_obj.send_email_alert(fd_obj)






