from twilio.rest import Client
import smtplib
import os
import requests


SHEETY_ENDPOINT = "https://api.sheety.co"
BEARER_AUTH = f'Bearer {os.environ["BEARER_AUTH"]}'
APIKEY = os.environ["SHEETY_APIKEY"]


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self.auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.client = Client(self.account_sid, self.auth_token)
        self.email = os.environ["FROM_EMAIL"]
        self.passwd = os.environ["EMAIL_PASSWD"]
        self.headers = {
            "Authorization": BEARER_AUTH
        }

    def send_sms_alert(self, fd):
        if fd.stop_overs == 0:
            message = self.client.messages.create(
                body=f"Low price alert! \n"
                     f"Only ₹{fd.price} from \n"
                     f"{fd.origin_city}-{fd.origin_airport_code} to {fd.destination_city}-{fd.destination_airport_code},from \n"
                     f"{fd.inbound_date} to {fd.outbound_date}",
                from_='FROM_NUMBER',
                to='TO_NUMBER')
        else:
            message = self.client.messages.create(
                body=f"Low price alert! \n"
                     f"Only ₹{fd.price} from \n"
                     f"{fd.origin_city}-{fd.origin_airport_code} to {fd.destination_city}-{fd.destination_airport_code},from \n"
                     f"{fd.inbound_date} to {fd.outbound_date}\n"
                     f"Flight has 1 stop over, via {fd.via_city}",
                from_='FROM_NUMBER',
                to='TO_NUMBER')

        print(message.status)

    def send_email_alert(self, fd):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/{APIKEY}/flightDeals/users",
                                headers=self.headers)
        users_dict = response.json()
        for user in users_dict['users']:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.email, password=self.passwd)
                if fd.stop_overs == 0:
                    connection.sendmail(from_addr=self.email,
                                        to_addrs=user['email'],
                                        msg="Subject:Low price alert\n\n"
                                            f"Only Rs{fd.price} from \n"
                                            f"{fd.origin_city}-{fd.origin_airport_code} to {fd.destination_city}-{fd.destination_airport_code},from \n"
                                            f"{fd.inbound_date} to {fd.outbound_date}")
                else:
                    connection.sendmail(from_addr=self.email,
                                        to_addrs=user['email'],
                                        msg="Subject:Low price alert\n\n"
                                            f"Only Rs{fd.price} from \n"
                                            f"{fd.origin_city}-{fd.origin_airport_code} to {fd.destination_city}-{fd.destination_airport_code},from \n"
                                            f"{fd.inbound_date} to {fd.outbound_date}\n"
                                            f"Flight has 1 stop over, via {fd.via_city}")

