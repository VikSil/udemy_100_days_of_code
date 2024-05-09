import requests
from pathlib import Path
from environ import Env
from twilio.rest import Client

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

WEATHER_API_KEY = env('WEATHER_API_KEY')
LOCATION = 'Oxford,UK'
LOCATION_LAT = 51.752022
LOCATION_LONG = -1.257726

FROM_PHONE_NUMBER = env('TWILIO_PHONE')
TO_PHONE_NUMBER = env('PHONE_NUMBER')
TWILIO_SID = env('TWILIO_SID')
TWILIO_API_KEY = env('TWILIO_API_KEY')


def main():

    weather_ids = get_weather_ids()
    will_rain = check_for_rain(weather_ids)

    if will_rain:
        send_sms('Кажется дождь собирается...')
    else:
        send_sms('Not a cloud in sight')


def get_weather_ids():
    # get three hourly weather forecast for the next 15 hours
    parameters = {
        'lat': LOCATION_LAT,
        'lon': LOCATION_LONG,
        'appid': WEATHER_API_KEY,
        'cnt': 5,
    }

    response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=parameters)
    response.raise_for_status()  # returns an error if the request failed
    data = response.json()
    return [weather['id'] for forecast in data['list'] for weather in forecast['weather']]


def check_for_rain(weather_ids):
    if all(x >= 700 for x in weather_ids):
        return False
    return True


def send_sms(msg):

    account_sid = TWILIO_SID
    auth_token = TWILIO_API_KEY
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=msg, from_=FROM_PHONE_NUMBER, to=TO_PHONE_NUMBER)

    print(message.status)


if __name__ == "__main__":
    main()
