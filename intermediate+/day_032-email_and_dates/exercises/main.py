import random
import smtplib
import datetime as dt
from pathlib import Path
from environ import Env


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR / 'variables.env')
env = Env()
env.read_env(BASE_DIR / 'variables.env')

FROM_EMAIL = env('FROM_EMAIL')
TO_EMAIL = env('TO_EMAIL')
APP_PSW = env('APP_PSW')


def main():

    now = dt.datetime.now()
    if now.weekday() == 0:
        with open(BASE_DIR/'exercises/quotes.txt') as file:
            quotes = file.readlines()

        todays_quote = random.choice(quotes)
        subject = 'Motivational Quote'

        with smtplib.SMTP('smtp.gmail.com', port = 587) as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=APP_PSW)
            connection.sendmail(from_addr=FROM_EMAIL, to_addrs=TO_EMAIL, msg=f'Subject:{subject}\n\n{todays_quote}')


if __name__ == "__main__":
    main()
