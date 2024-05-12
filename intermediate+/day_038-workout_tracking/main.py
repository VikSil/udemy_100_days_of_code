import requests
from environ import Env
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

NUTRI_API_KEY = env('NUTRI_API_KEY')
NUTRI_APP_ID = env('NUTRI_APP_ID')
NUTRI_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'

SHEETY_API_KEY = env('SHEETY_API_KEY')
SHEETY_API_USERNAME = env('SHEETY_API_USERNAME')
SHEETY_API_PSW = env('SHEETY_API_PSW')
SHEETY_ENDPOINT = 'https://api.sheety.co/dfdcdc797cdebfcdb558cf9268d62251/udemyWorkouts/workouts'
SHEETY_WORKSHEET = 'workout'

GENDER = 'female'
WEIGHT_KG = 66
HEIGHT_CM = 155
AGE = 39


def main():
    exercise_stats = get_exercise_stats()

    for stats in exercise_stats['exercises']:
        post_exercise_stats(stats)


def post_exercise_stats(stats):

    date = datetime.now().strftime('%d/%m/%Y')
    time = datetime.now().strftime('%X')

    headers = {'Authorization': f'Bearer {SHEETY_API_KEY}'}

    parameters = {
        SHEETY_WORKSHEET: {
            'date': date,
            'time': time,
            'exercise': stats['name'].title(),
            'duration': stats['duration_min'],
            'calories': stats['nf_calories'],
        }
    }

    response = requests.post(SHEETY_ENDPOINT, headers=headers, json=parameters)
    print(response.text)


def get_exercise_stats():

    nat_lang_input = input('What exercises did you do today? ')

    headers = {
        'x-app-id': NUTRI_APP_ID,
        'x-app-key': NUTRI_API_KEY,
    }

    parameters = {'query': nat_lang_input, 'gender': GENDER, 'weight_kg': WEIGHT_KG, 'height_cm': HEIGHT_CM, 'age': AGE}

    response = requests.post(NUTRI_ENDPOINT, headers=headers, json=parameters)
    result = response.json()
    print(result)
    return result


if __name__ == "__main__":
    main()
