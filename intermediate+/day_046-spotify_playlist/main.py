import requests
from bs4 import BeautifulSoup
from pathlib import Path
from environ import Env
from datetime import datetime
from typing import List, Tuple
import spotipy
from spotipy.oauth2 import SpotifyOAuth


BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'variables.env')

SPOTIPY_CLIENT_ID = env('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = env('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = env('SPOTIPY_REDIRECT_URI')


def main():
    user_input = get_input()
    songs = scrape_data(user_input)

    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope="playlist-modify-private",
            cache_path="token.txt",
        )
    )
    user = spotify.me()

    song_uris = get_spotify_uris(spotify, songs, user_input[:4])

    playlist = spotify.user_playlist_create(user['id'], f'{user_input} Billboard 100', False)
    if len(song_uris) > 0:
        spotify.user_playlist_add_tracks(user['id'], playlist['id'], song_uris)


def get_input() -> str:

    got_date = False

    while not got_date:
        user_input = input("Please input a past date of 4th Aug 1958 or later in format YYYY-MM-DD\n")

        if check_date(user_input):
            got_date = True
        else:
            print("Wrong date format!")

    return user_input


def check_date(date_str: str) -> bool:
    format = '%Y-%m-%d'
    try:
        date = datetime.strptime(date_str, format)
    except ValueError:
        return False

    return date >= datetime(1958, 8, 4) and date <= datetime.now()


def scrape_data(date_str: str) -> List[Tuple]:
    url = f'https://www.billboard.com/charts/hot-100/{date_str}'
    response = requests.get(url)
    website_html = BeautifulSoup(response.content.decode('utf-8', 'ignore'))

    chart_lines = website_html.find_all(name='div', class_='o-chart-results-list-row-container')
    titles = [line.find(name='h3').getText().strip() for line in chart_lines]
    artists = [line.find(name='h3').next_sibling.next_sibling.getText().strip() for line in chart_lines]

    songs = list(zip(titles, artists))
    return songs


def get_spotify_uris(spotify: spotipy.client.Spotify, songs: List[Tuple], year: str) -> List[str]:
    song_uris = []
    for song in songs:
        title = song[0].replace(' ', '%2520')
        artist = song[1].replace(' ', '%2520')
        track = spotify.search(q=f'artist%3{artist}%2520track%3{title}%2520year%3{year}', type='track', limit=1)
        try:
            song_uris.append(track['tracks']['items'][0]['uri'])
        except IndexError:
            print(f"Spotify does not know this song: {song[1]} - {song[0]}")

    return song_uris


if __name__ == "__main__":
    main()
