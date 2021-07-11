import requests
from config import *
from spotipy import oauth2
from os.path import exists, abspath

SPOTIFY_GET_CURRENT_TRACK = "https://api.spotify.com/v1/me/player/currently-playing"

def get_access_token() -> str:
    sp_oauth = oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                   redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)
    code = sp_oauth.get_access_token()

    return code['access_token']

def get_current_track(access_token=None) -> dict:
    if not access_token:
        access_token = get_access_token()

    resp = requests.get(
        SPOTIFY_GET_CURRENT_TRACK,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if resp.status_code == 200:
        resp_json = resp.json()
        return {
            "track_id": resp_json['item']['id'],
            "track_name": resp_json['item']['name'],
            "artists":  ", ".join([artist['name'] for artist in resp_json['item']['artists']]),
            "album": resp_json['item']['album']['name'],
            "cover": resp_json['item']['album']['images']
        }
    else:
        print(f"Status code: {resp.status_code}. Something went wrong :(")
        return {}


class ImageSwapper:
    @staticmethod
    def swap(url: str) -> str:
        name = CACHE_FOLDER + '/' + url.split('/')[-1] + ".jpeg"
        if not exists(name):
            req = requests.get(url)
            if req.status_code == 200:
                with open(name, 'wb') as wf:
                    for ch in req:
                        wf.write(ch)
                return abspath(name)
