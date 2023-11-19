#file that holds stuff to ping detection on webcam

import os
from dotenv import load_dotenv
from twilio.rest import Client #type: ignore
import twilio #type: ignore
from database.data import data_commands as DATA


load_dotenv('.env')
Data = DATA()

account_sid = os.getenv('SMS_ACCOUNT_SID')
auth_token = os.getenv('SMS_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_alert():
    recipient_number = Data.get_phone_number()
    if recipient_number == None:
        print("phone number not found")
        return
    try:
        message = client.messages \
                    .create(
                        body="Motion has been detected on your webcam",
                        from_='SMS_SENDER_NUMBER',
                        to=recipient_number
                    )
    except twilio.TwilioRestException as e:
        print(e)

if __name__ == "__main__":
    send_alert()
