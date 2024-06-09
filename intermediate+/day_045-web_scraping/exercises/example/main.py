from bs4 import BeautifulSoup
from pathlib import Path


def main():
    BASE_DIR = Path(__file__).resolve().parent

    with open(BASE_DIR / "website.html", encoding="utf8") as f:
        soup = BeautifulSoup(f, 'html.parser')

        print(soup.title.string)


if __name__ == "__main__":
    main()
