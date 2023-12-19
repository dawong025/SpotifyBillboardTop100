from bs4 import BeautifulSoup
import requests, spotipy
from spotipy import SpotifyOAuth



year = "2010"
day = "01"
month = "01"
date = year + "-" + month + "-" + day


response = requests.get("https://billboard.com/charts/hot-100/" + date)
# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')
song_name_spans = soup.select('li ul li h3')
song_names = [song.getText().strip() for song in song_name_spans]

artist_spans = soup.find_all(name="span", class_="a-no-trucate")
artist_names = [artist.getText().strip() for artist in artist_spans]


sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = "playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id='YOUR CLIENT ID HERE',
        client_secret='YOUR CLIENT SECRET HERE',
        show_dialog=True,
        cache_path="token.txt",
        username="YOUR USERNAME HERE"
    )
)
user_id = sp.current_user()['id']
song_uris = []

for item in range(0, len(song_names)):
    print(song_names[item] + " - " + artist_names[item])
    result = sp.search(q="artist" + artist_names[item] + "track:" + song_names[item], type = "track")
    # print(result)

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song_names[item]} doesnt exist on Spotify")

playlist = sp.user_playlist_create(user = user_id, name=f"{year} Test Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Success")


