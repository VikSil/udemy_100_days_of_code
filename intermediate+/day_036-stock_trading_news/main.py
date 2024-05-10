import requests
from environ import Env
from pathlib import Path
from twilio.rest import Client
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

TICKER = "ARHS"
ISSUER = "Arhaus"

FROM_PHONE_NUMBER = env('TWILIO_PHONE')
TO_PHONE_NUMBER = env('PHONE_NUMBER')
TWILIO_SID = env('TWILIO_SID')
TWILIO_API_KEY = env('TWILIO_API_KEY')

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = env('ALPHA_API_KEY')
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = env('NEWS_API_KEY')

def main():

    ## STEP 1: Use https://www.alphavantage.co/query
    # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    # HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 20 - 40 = -20, but the positive difference is 20.
    # HINT 2: Work out the value of 5% of yesterday's closing stock price.

    time_t = datetime.now().date()
    time_t_minus_one = str(time_t - timedelta(days=1))
    time_t_minus_two = str(time_t - timedelta(days=2))

    prices = get_close_price(TICKER)
    close_t_minus_one = float(prices[time_t_minus_one]['4. close'])
    close_t_minus_two = float(prices[time_t_minus_two]['4. close'])
    change = get_change(close_t_minus_two, close_t_minus_one)

    ## STEP 2: Use https://newsapi.org/docs/endpoints/everything
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
    # HINT 3: Think about using the Python Slice Operator

    if change['percentage'] >= 5:
        news = get_news(ISSUER)

        ## STEP 3: Use twilio.com/docs/sms/quickstart/python
        # Send a separate message with each article's title and description to your phone number.

        for article in news: 
            send_sms(TICKER, change['is_bullish'], change['percentage'], article['title'], article['description'])


def get_close_price(ticker):
    parameters = {'function': 'TIME_SERIES_DAILY', 'symbol': ticker, 'apikey': STOCK_API_KEY}

    response = requests.get(STOCK_ENDPOINT, params=parameters)
    response.raise_for_status()  # returns an error if the request failed
    data = response.json()
    return data['Time Series (Daily)']


def get_change(price1, price2):
    diff = abs(price1 - price2)
    if price1 < price2:
        is_bullish = True
    else:
        is_bullish = False
    percentage = round(((diff * 100) / price1), 2)

    return {'difference': diff, 'is_bullish': is_bullish, 'percentage': percentage}


def get_news(company):
    parameters = {'q': company, 'apikey': NEWS_API_KEY, 'sorted_by': 'popularity'}

    response = requests.get(NEWS_ENDPOINT, params=parameters)
    response.raise_for_status()  # returns an error if the request failed
    data = response.json()
    return data['articles'][:3]


def send_sms(ticker, growing, change, headline, brief):

    # Optional: Format the SMS message like this:
    """
    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    or
    "TSLA: 🔻5%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    """

    if growing:
        emoji = '🔺'
    else:
        emoji = '🔻'

    msg = f'{ticker} {emoji}{change}%\nHeadline: {headline}\nBrief: {brief}'

    account_sid = TWILIO_SID
    auth_token = TWILIO_API_KEY
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=msg, from_=FROM_PHONE_NUMBER, to=TO_PHONE_NUMBER)
    print(message.status)


if __name__ == "__main__":
    main()
