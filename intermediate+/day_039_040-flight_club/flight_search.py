import requests
from environ import Env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')


class FlightSearch:

    def __init__(self):
        self.api_key = env('RAPID_API_KEY')
        self.airports_endpoint = 'https://priceline-com-provider.p.rapidapi.com/v1/flights/locations'
        self.airport_host = 'priceline-com-provider.p.rapidapi.com'
        self.flights_endpoint = 'https://booking-com18.p.rapidapi.com/flights/search-oneway'
        self.flights_host = 'booking-com18.p.rapidapi.com'

    def get_airport_codes(self, location):
        '''
        Function takes city name and returns all airports in that city
        '''
        headers = {'X-RapidAPI-Key': self.api_key, 'X-RapidAPI-Host': self.airport_host}
        params = {'name': location}
        response = requests.get(self.airports_endpoint, headers=headers, params=params)
        return response.json()

    def get_flights(self, from_code, to_code, date, max_price):
        '''
        Function gets all flights from and to airport codes on a given date that cost less than given price
        '''
        headers = {'X-RapidAPI-Key': self.api_key, 'X-RapidAPI-Host': self.flights_host}
        params = {
            'fromId': from_code,
            'toId': to_code,
            'departureDate': date,
            'priceRange': f'0,{max_price}',
        }
        response = requests.get(self.flights_endpoint, headers=headers, params=params)
        return response.json()['data']['flights']
