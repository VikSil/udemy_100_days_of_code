##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.


import random
import smtplib
import pandas as pd
import datetime as dt
from pathlib import Path
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

FROM_EMAIL = env('FROM_EMAIL')
APP_PSW = env('APP_PSW')

def main():

    birthdays = pd.read_csv(BASE_DIR / 'project/birthdays.csv')
    now = dt.datetime.now()
    has_birthday = birthdays.loc[(birthdays['month'] == now.month) & (birthdays['day'] == now.day)]
    if not has_birthday.empty:
        recipients = has_birthday['name']
        templates = ['letter_1.txt','letter_2.txt', 'letter_3.txt']
        for recipient in recipients:
            with open(f'{BASE_DIR}/project/letter_templates/{random.choice(templates)}') as file:
                text = file.read()

            text = text.replace('[NAME]', recipient)
            subject = 'Happy Birthday!'
            email = birthdays.loc[(birthdays['name'] == recipient)].iloc[0]['email']

            with smtplib.SMTP('smtp.gmail.com', port = 587) as connection:
                connection.starttls()
                connection.login(user=FROM_EMAIL, password=APP_PSW)
                connection.sendmail(from_addr=FROM_EMAIL, to_addrs=email, msg=f'Subject:{subject}\n\n{text}')

if __name__ == "__main__":
    main()
