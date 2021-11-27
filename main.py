import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "fc39e958aad241e2a3b912be42c85fe1"
CLIENT_SECRET="74b0c1a7384d432b837454d88e01d205"
SPOTIPY_ENDPOINT= "https://accounts.spotify.com/api/token"

date = input("which year do u wanna listen to? Enter in YYYY-MM-DD format:")
CLASS_SONG={
    "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16" +
    " u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"
}
URL="https://www.billboard.com/charts/hot-100/"+ date + "/"

response = requests.get(URL)
website_data = response.text
song_urls = []
soup = BeautifulSoup(website_data,"html.parser")
soup.titles = soup.find_all(id="title-of-a-story")
soup.songs = [song.getText() for song in soup.titles]
print(soup.songs)
with open("songlist.txt", mode="w") as name:
    for songs in soup.songs:
        name.write(songs)
        song_urls.append(songs)


'''scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

params={
         "client_id" : CLIENT_ID ,
         "client_secret" : CLIENT_SECRET,
         "redirect_url" : " http://example.com",

}'''


SP = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    ))

user_id = SP.current_user()["id"]

print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in soup.songs:
    result = SP.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = SP.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
SP.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
