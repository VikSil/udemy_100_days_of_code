import re
import smtplib
import requests
from environ import Env
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup


URL = 'https://www.amazon.com/CanaKit-Raspberry-8GB-Starter-Kit/dp/B08956GVXN'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
THRESHOLD = 150

BASE_DIR = Path(__file__).resolve().parent

env = Env()
env.read_env(BASE_DIR / 'variables.env')
FROM_EMAIL = env('FROM_EMAIL')
TO_EMAIL = env('TO_EMAIL')
APP_PSW = env('APP_PSW')


def main():
    soup = scrape_amazon_page()
    price = get_price(soup)
    title = get_product_title(soup)

    if not price or not title:
        send_alert(
            f'Subject:Check the Amazon price checking script\n\nThe script failed to find either price or title. Check if the Amazon product layout still is the same.'
        )
    elif price < THRESHOLD:
        send_alert(
            f'Subject:Price for {title} fallen below {THRESHOLD}\n\n Good news!\n\nThe price for {title} is {price} today.\nLink to Amazon: {URL}'
        )


def scrape_amazon_page() -> BeautifulSoup:

    # works without headers as well, at least on Kali
    response = requests.get(URL, headers=HEADERS)
    # works with html parser as well as lxml - slightly different outputs, but the span tag is the same
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')

    return soup


def get_price(soup: BeautifulSoup) -> Optional[float]:
    pricetag = soup.find(name='span', class_='a-offscreen').getText()

    try:
        numbers = float(re.search('\d+.\d\d', pricetag).group(0))
    except AttributeError:
        numbers = None

    return numbers


def get_product_title(soup: BeautifulSoup) -> Optional[str]:
    span = soup.find(
        name='span', class_='a-size-large product-title-word-break', id='productTitle'
    )
    text = span.getText().strip()
    return text


def send_alert(text: str) -> None:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=FROM_EMAIL, password=APP_PSW)
        connection.sendmail(from_addr=FROM_EMAIL, to_addrs=TO_EMAIL, msg=text)


if __name__ == '__main__':
    main()
