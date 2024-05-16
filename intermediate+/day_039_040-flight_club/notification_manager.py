from environ import Env
from pathlib import Path
from twilio.rest import Client

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

class NotificationManager:
    def __init__(self):
        self.account_sid = env('TWILIO_SID')
        self.api_key = env('TWILIO_API_KEY')
        self.from_phone = env('TWILIO_PHONE_NUMBER')
        self.to_phone = env('MY_PHONE_NUMBER')
        self.client = Client(self.account_sid, self.api_key)

    def send_alert(self, price, destination, date, url):
        '''
        Function sends an sms alert about a cheap flight
        '''
        msg = f'Low price alert! Only ${price} to fly from London to {destination} on {date}. {url}'
        message = self.client.messages.create(body=msg, from_=self.from_phone, to=self.to_phone)
        print(message.status)
