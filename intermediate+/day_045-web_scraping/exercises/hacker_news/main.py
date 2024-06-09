from bs4 import BeautifulSoup as bs
import requests


def main():

    response = requests.get('https://news.ycombinator.com/news')
    yc_web_page = response.text

    soup = bs(yc_web_page, 'html.parser')
    link_spans = soup.find_all(name='span', class_='titleline')
    link_hrefs = [span.contents[0]['href'] for span in link_spans]
    link_texts = [span.contents[0].getText() for span in link_spans]

    score_spans = soup.find_all(name='span', class_='score')
    scores = [int(span.getText().split()[0]) for span in score_spans]
    max_score_index = scores.index(max(scores))

    print(link_texts[max_score_index])
    print(link_hrefs[max_score_index])
    print('score: ', scores[max_score_index])


if __name__ == "__main__":
    main()
