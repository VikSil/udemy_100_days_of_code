import requests
from environ import Env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')


class DataManager:
    def __init__(self):
        self.api_key = env('SHEETY_API_KEY')
        self.api_username = env('SHEETY_API_USERNAME')
        self.api_psw = env('SHEETY_API_PSW')
        self.endpoint = 'https://api.sheety.co/dfdcdc797cdebfcdb558cf9268d62251/udemyFlightClub/sheet1'
        self.worksheet = 'sheet1'

    def get_all_data(self):
        '''
        Function returns all data in the spreadsheet
        '''
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(self.endpoint, headers=headers)
        return response.json()[self.worksheet]

    def update_rows(self, new_data):
        '''
        Function takes a list of lines as dictionaries and updates all iata codes in spreadsheet
        '''
        headers = {'Authorization': f'Bearer {self.api_key}'}

        for line in new_data:
            params = {
                self.worksheet: {
                    'iataCode': line['iataCode'],
                }
            }
            url = f'{self.endpoint}/{line["id"]}'
            requests.put(url, headers=headers, json=params)
