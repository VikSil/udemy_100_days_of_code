import smtplib
from environ import Env
from pathlib import Path
from twilio.rest import Client

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')


class NotificationManager:
    def __init__(self):
        self.sms_account_sid = env('TWILIO_SID')
        self.sms_api_key = env('TWILIO_API_KEY')
        self.from_phone = env('TWILIO_PHONE_NUMBER')
        self.to_phone = env('MY_PHONE_NUMBER')
        self.sms_client = Client(self.sms_account_sid, self.sms_api_key)
        self.email_psw = env('EMAIL_PSW')
        self.from_email = env('FROM_EMAIL')

    def send_sms_alert(self, price, destination, date, url):
        '''
        Function sends an sms alert about a cheap flight
        '''
        msg = f'Low price alert! Only ${price} to fly from London to {destination} on {date}. {url}'
        message = self.sms_client.messages.create(body=msg, from_=self.from_phone, to=self.to_phone)
        print(message.status)

    def send_email(self, email, subject, text):
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(self.from_email, self.email_psw)
            connection.sendmail(from_addr=self.from_email, to_addrs=email, msg=f'Subject:{subject}\n\n{text}')
