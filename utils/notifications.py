#file that holds stuff to ping detection on webcam

import os
from dotenv import load_dotenv
from twilio.rest import Client
from database.data import data_commands as Data


load_dotenv()
Data()

account_sid = 'SMS_ACCOUNT_SID'
auth_token ='SMS_AUTH_TOKEN'
client = Client(account_sid, auth_token)

def send_alert():
    recipient_number = Data.get_phone_number()
    if recipient_number == None:
        print("number not found")
        return
    
    message = client.messages \
                .create(
                     body="Motion has been detected on your webcam",
                     from_='SMS_SENDER_NUMBER',
                     to=recipient_number
                 )


