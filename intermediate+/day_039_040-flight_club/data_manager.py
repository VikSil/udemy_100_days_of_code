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
        self.endpoint = 'https://api.sheety.co/dfdcdc797cdebfcdb558cf9268d62251/udemyFlightClub/'
        self.worksheet = 'sheet1'
        self.worksheet_users = 'sheet2'

    def get_destination_data(self):
        '''
        Function returns all flight data in the spreadsheet
        '''
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(f'{self.endpoint}/{self.worksheet}', headers=headers)
        return response.json()[self.worksheet]

    def get_user_data(self):
        '''
        Function returns all signed up user data in the spreadsheet
        '''
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(f'{self.endpoint}/{self.worksheet_users}', headers=headers)
        return response.json()[self.worksheet_users]

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
            url = f'{self.endpoint}/{self.worksheet}/{line["id"]}'
            requests.put(url, headers=headers, json=params)

    def add_user(self, first_name, last_name, email):
        '''
        Function adds a new user to the spreadsheet
        '''
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {
            self.worksheet_users: {
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
            }
        }

        response = requests.post(f'{self.endpoint}/{self.worksheet_users}', headers=headers, json=params)
