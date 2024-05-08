import time
import smtplib
import requests
from environ import Env
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = Env()
env.read_env(BASE_DIR / 'day_032-email_and_dates/variables.env')


LOCATION_LONG = -1.257726
LOCATION_LAT = 51.752022
FROM_EMAIL = env('FROM_EMAIL')
TO_EMAIL = env('TO_EMAIL')
APP_PSW = env('APP_PSW')

def main():
    # Find out ISS current location
    response = requests.get(url = 'http://api.open-notify.org/iss-now.json')
    response.raise_for_status() # returns an error if the request failed
    data = response.json()
    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])

    # find out sunrise and sunset times in my location
    parameters = {'lng': LOCATION_LONG, 'lat': LOCATION_LAT, 'formatted': 0}
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']


    # If the ISS is close to my current position
    # and it is currently dark
    # Then send an email saying to look up.

    long_distance = longitude_distance(iss_longitude, LOCATION_LONG)

    if long_distance <= 5: 
        lat_distance = latitude_distance(iss_latitude, LOCATION_LAT)

        if lat_distance <= 5: 
            if is_nightime(sunrise, sunset):
                subject = 'ISS is above you'
                text = 'Look up!'

                with smtplib.SMTP('smtp.gmail.com', port = 587) as connection:
                    connection.starttls()
                    connection.login(user=FROM_EMAIL, password=APP_PSW)
                    connection.sendmail(from_addr=FROM_EMAIL, to_addrs=TO_EMAIL, msg=f'Subject:{subject}\n\n{text}')
                print('Look Up!')
            else:
                print('The ISS may be above you, but it is too light to see it')
        else:
            print('The ISS is nowhere near you.')
    else:
        print('The ISS is nowhere near you.')


def longitude_distance(long1, long2):
    # longitude distance calculations
    # if same sign - substract and take absolute value
    # if oposite signs - find minimum between absolute longitude and 180 - absolute longitude for both and take sum

    if (long1 > 0 and long2 > 0) or (long1 < 0 and long2 < 0):
        return abs(long1 - long2)
    else:
        return min(abs(long1), (180 - abs(long1))) +  min(abs(long2), (180 - abs(long2)))


def latitude_distance(lat1, lat2):
    # latitude distance calculations
    # if same sign - substract and take absolute value
    # if diiferent signs - abs individualy and take sum - since poles don't wrap around to each other

    if (lat1 > 0 and lat2 > 0) or (lat1 < 0 and lat2 < 0):
        return abs(lat1 - lat2)
    else:
        return abs(lat1) + abs(lat2)


def is_nightime(sunrise, sunset):
    sunrise_hour = int(sunrise.split('T')[1].split(':')[0])
    sunrise_minute = int(sunrise.split('T')[1].split(':')[1])
    sunset_hour = int(sunset.split('T')[1].split(':')[0])
    sunset_minute = int(sunset.split('T')[1].split(':')[1])
    now = datetime.now()

    # check if dayime
    if (sunrise_hour < now.hour and sunset_hour > now.hour) or (sunrise_hour == now.hour and sunrise_minute < now.minute) or (sunset_hour == now.hour and sunset_minute > now.minute):
          return False
    
    return True

if __name__ == "__main__":

    # BONUS: run the code every 60 seconds.
    while True:
        time.sleep(60)
        main()

