import requests
from bs4 import BeautifulSoup
from pathlib import Path


URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
BASE_DIR = Path(__file__).resolve().parent

# Write your code below this line 👇


def main():
    response = requests.get(URL)
    website_html = BeautifulSoup(response.content.decode('utf-8', 'ignore'))

    h3_list = website_html.find_all(name='h3', class_='title')
    # movie 12 has title formatted with ':' instead of ')'
    # movie 21 starts with numbers and collon - 2001: A Space Odyssey
    # hence, leftstrip all numbers, then leftstrip a space
    titles = [title.getText().lstrip('0123456789):').lstrip() for title in reversed(h3_list)]
    renumbered_titles = [str(index + 1) + '. ' + title for index, title in enumerate(titles)]

    with open(BASE_DIR / 'movies.txt', 'w', encoding='utf-8') as file:
        for item in renumbered_titles:
            file.write(f'{item}\n')


if __name__ == "__main__":
    main()
