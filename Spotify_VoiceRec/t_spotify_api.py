from http import HTTPStatus
from dotenv import load_dotenv

import requests # HTTP Client Library 
import base64 
import os


""" Basic query of Spotify API,
    Retrieving a specific songtitle, artist and song URL.

    Moving forward, this project will include STT (Speech-To-Text), with a wake word
    for the Raspberry PI, to further query it to play a specific song 
"""

# This program needs CLIENT_ID and CLIENT_SECRET from your own Spotify App
# Load these 
load_dotenv()


# TODO: Create as async
def get_token():
    url = 'https://accounts.spotify.com/api/token'

    # Retrieve client_id and client_secret from .env
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode() 

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == HTTPStatus.OK:
        token_info = response.json()
        return token_info['access_token']
    else:
        print(f"Failed to retrieve token: {response.status_code} - {response.text}")
        return None 
    

def search_by_song(token):
    url = "https://api.spotify.com/v1/search"

    # Build query parameters. %20 --> Space (Cry For Me)
    params = {
        "q": 'remaster%20track:Cry%20For%20Me%20artist:The%20Weeknd&type=track&limit=1',
        "type": "track"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        tracks = data['tracks']['items']
        track = tracks[0] # Retrieve first result, assuming correct artist and song title
        print(f"Song: {track['name']}. Artist: {track['artists'][0]['name']}. Link: {track['external_urls']['spotify']}")
    else:
        print(f"Failed to retrieve results: {response.status_code} - {response.text}")
        return None 
    
if __name__ == "__main__": 
    s_token = get_token()
    search_by_song(s_token)