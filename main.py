from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import SpotifyOAuth
import time

year = "2010"
day = "01"

all_artist_names = []
all_song_names = []

for month in range(1, 13):
    # print(month)
    if len(str(month)) == 1:
        str_month = "0" + str(month)
    else:
        str_month = str(month)

    date = year + "-" + str_month + "-" + day

    response = requests.get("https://billboard.com/charts/hot-100/" + date)
    # print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    song_name_spans = soup.select('li ul li h3')
    song_names = [song.getText().strip() for song in song_name_spans]
    all_song_names.extend(song_names)

    artist_spans = soup.find_all(name="span", class_="a-no-trucate")
    artist_names = [artist.getText().strip() for artist in artist_spans]
    all_artist_names.extend(artist_names)

    month += 1

print(len(all_artist_names))

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = 'playlist-modify-private',
        redirect_uri='https://example.com/',
        client_id='',
        client_secret='',
        show_dialog=True,
        cache_path='token.txt',
        username=''
    )
)
user_id = sp.current_user()['id']
song_uris = []
print(len(song_uris))

for item in range(0, len(all_song_names)):
    if item % 100 == 0:
        print("Milestone: " + str(item))
        time.sleep(30)
        print("Sleep done") # workaround for Spotify API rate limit
    # print(all_song_names[item] + " - " + all_artist_names[item])
    # print(all_artist_names[item] + " - " + all_song_names[item])
    result = sp.search(q=all_artist_names[item] + "-" + all_song_names[item], type = "track")
    # print(str(result["tracks"]["items"][0]["artists"][0]["name"]) + " - " + str(result["tracks"]["items"][0]['name']))

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{all_song_names[item]} doesnt exist on Spotify")

print("Done Searching")
playlist = sp.user_playlist_create(user = user_id, name=f"{year} Test Billboard 100", public=False)

floor = 0
ceiling = 100
loop_num = 0
if len(all_song_names) % 100 == 0:
    loop_num = int(len(all_song_names)/100)
else: #handle the remainders
    loop_num = int(len(all_song_names)/100) + 1
# work around for Spotify API rate limit, break adding songs from array req to every 100
for i in range(0, loop_num):
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris[floor:ceiling])
    floor = ceiling
    if len(all_song_names) - ceiling < 100: # when there are dupes, len may not be 1200
        ceiling += len(all_song_names) - ceiling # set ceiling to the remaining songs in the list
    else:
        ceiling += 100

print("Success")
