import requests
from environ import Env
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

API_KEY = env('API_KEY')
API_USER = env('API_USER')
USERS_ENDPOINT = 'https://pixe.la/v1/users'
GRAPH_ID = 'codingtime'
GRAPH_ENDPOINT = f'{USERS_ENDPOINT}/{API_USER}/graphs'
UPDATE_GRAPH_ENDPOINT = f'{USERS_ENDPOINT}/{API_USER}/graphs/{GRAPH_ID}'


def main():
    # create_user()
    # create_graph()
    add_time(300)


def add_time(minutes):

    today = datetime.now().date().strftime('%Y%m%d')

    headers = {'X-USER-TOKEN': API_KEY}

    parameters = {
        'date': today,
        'quantity': str(minutes),
    }

    response = requests.post(UPDATE_GRAPH_ENDPOINT, json=parameters, headers=headers)
    response.raise_for_status()  # returns an error if the request failed
    print(response.text)


def create_graph():
    headers = {'X-USER-TOKEN': API_KEY}

    parameters = {
        'id': GRAPH_ID,
        'name': 'Coding Time',
        'unit': 'minute',
        'type': 'int',
        'color': 'ajisai',
    }

    response = requests.post(GRAPH_ENDPOINT, json=parameters, headers=headers)
    response.raise_for_status()  # returns an error if the request failed
    print(response.text)


def create_user():
    parameters = {
        'token': API_KEY,
        'username': API_USER,
        'agreeTermsOfService': 'yes',
        'notMinor': 'yes',
    }

    response = requests.post(USERS_ENDPOINT, json=parameters)
    response.raise_for_status()  # returns an error if the request failed
    print(response.text)


if __name__ == "__main__":
    main()
