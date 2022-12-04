from bs4 import BeautifulSoup
import requests
import spotipy 
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "e440ef0e20c24451809a360b6c56999c"
CLIENT_SECRET = "8bd8d834df8e49dbab2a177327ea3011"

date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD")
URL = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

songs = soup.select("li ul li h3")
song_list = []

for song in songs:
    song_list.append(song.get_text().strip())


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

search_years = f"{int(year)-1}-{year}"

for song in song_list:
    result = sp.search(q = f"track:{song} year:{search_years}", type = "track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user = user_id, name = f"{date} Billboard Top 100", public = False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print("Playlist Created")


