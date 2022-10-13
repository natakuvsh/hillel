import datetime
import sqlite3
import requests
from models import Song,Artist


DATABASE_LOCATION = "sqlite:///songs_library.sqlite3"
USER_ID = "31gszperdeihwxlmazxngke5npca"
TOKEN = "BQDjHVrmIruK64LGF98mX6gaRhtSxlKUfki9gZM515Q_fQm1d_xpMZY4EH7Dr-g1hRyubM1Dp6uDhtxwqoiBwe2kRNWO67LZZ4eoX_QBk1ze_a4DZuSyoOgPr2rszKnwfZHjGAIXcNLTZige0ULeFz3P4iIfdaMtWu7fzf96sxQfswybjoC6UaeJCUr77yXtasrjjRn0"


if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played",headers=headers)
    data = r.json()

    ids = {}
    rows_songs = []
    rows_artists = []

    index = 1
    for song in data["items"]:
        song_data = {}
        artist_data = {}
        song_data['name'] = song["track"]["name"]
        song_data['duration'] = int(int(song["track"]["duration_ms"])/1000)
        artist = song["track"]["album"]["artists"][0]["name"]
        artist_data['name'] = artist

        if artist not in ids.values():
            ids[index] = artist
            song_data['artist'] = index
            index += 1
        else:
            song_data['artist'] = [k for k, v in ids.items() if v == artist][0]

        rows_songs.append(song_data)
        rows_artists.append(artist_data)

    Song.insert_many(rows_songs).execute()
    Artist.insert_many(rows_artists).execute()

