import os
from twilio.rest import Client
from django.conf import settings


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
def send_sms(user_code,phone_number):
    message = client.messages.create(
                                body=f'Hi! Your User ans Verification Code is {user_code}',
                                from_='+14847390943',
                                to=f'{phone_number}'
                            )

    # print(message)