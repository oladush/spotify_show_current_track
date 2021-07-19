"""
⠄⠰⠛⠋⢉⣡⣤⣄⡉⠓⢦⣀⠙⠉⠡⠔⠒⠛⠛⠛⠶⢶⣄⠘⢿⣷⣤⡈⠻⣧
⢀⡔⠄⠄⠄⠙⣿⣿⣿⣷⣤⠉⠁⡀⠐⠒⢿⣿⣿⣿⣶⣄⡈⠳⢄⣹⣿⣿⣾⣿
⣼⠁⢠⡄⠄⠄⣿⣿⣿⣿⡟⠄⡐⠁⡀⠄⠈⣿⣿⣿⣿⣿⣷⣤⡈⠻⣿⣿⣿⣿
⢻⡀⠈⠄⠄⣀⣿⣿⣿⡿⠃⠄⡇⠈⠛⠄⠄⣿⣿⣿⣿⣿⣿⠟⠋⣠⣶⣿⣿⣿ About Program: SpotifyCurrentShowTrack.py is a little program
⠄⢉⡓⠚⠛⠛⠋⣉⣩⣤⣤⣀⠑⠤⣤⣤⣾⣿⣿⣿⡿⠛⢁⣤⣾⣿⣿⣿⣿⣿                  who show current track from spotify
⠄⠈⠙⠛⠋⣭⣭⣶⣾⣿⣿⣿⣷⣦⢠⡍⠉⠉⢠⣤⣴⠚⢩⣴⣿⣿⣿⣿⣿⣿
⠄⢴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣭⣭⣥⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿ Versions: 0.0.0.0.1, pre build
⠄⣴⣶⡶⠶⠶⠶⠶⠶⠶⠶⠶⣮⣭⣝⣛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ Authors:  olad
⠄⠙⣿⡄⠄⠄⢀⡤⠬⢭⣝⣒⢂⠭⣉⠻⠿⣷⣶⣦⣭⡛⣿⣿⣿⣿⣿⣿⣿⣿ License:  not
⠄⠄⠸⣿⡇⠄⠸⣎⣁⣾⠿⠉⢀⠇⣸⣿⣿⢆⡉⠹⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿
⠄⠄⠄⣿⡇⠄⢀⡶⠶⠶⠾⠿⠮⠭⠭⢭⣥⣿⣿⣷⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿ Requirements: Requests, Pillow, Spotipy, Pyglet (if Win)
⠄⠄⠄⣿⡇⠄⠈⣷⠄⠄⠄⣭⣙⣹⢙⣰⡎⣿⢏⣡⣾⢏⣾⣿⣿⣿⣿⣿⣿⣿
⠄⠄⢰⣿⡇⠄⠄⢿⠄⠄⠈⣿⠉⠉⣻⣿⡷⣰⣿⡿⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⢸⣿⡇⠄⠄⠘⠿⠤⠤⠿⠿⠿⢤⣤⣤⡿⣃⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠄⠘⢿⣷⣤⣄⣀⣀⣀⣀⣀⣠⣴⣾⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋
"""


from config import *

import requests
from time import sleep
from spotipy import oauth2
from threading import Thread
from PIL import ImageTk, Image
from os.path import exists, abspath
from tkinter import Canvas, Label, Tk, Toplevel

#exceptions
from requests.exceptions import ConnectionError

SPOTIFY_GET_CURRENT_TRACK = "https://api.spotify.com/v1/me/player/currently-playing"


class SpotifyFuncs:
    @staticmethod
    def get_access_token() -> str:
        sp_oauth = oauth2.SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)

        code = sp_oauth.get_access_token()

        return code['access_token']

    @staticmethod
    def get_current_track(access_token=None) -> dict:
        if not access_token:
            access_token = SpotifyFuncs.get_access_token()

        try:
            resp = requests.get(
                SPOTIFY_GET_CURRENT_TRACK,
                headers={"Authorization": f"Bearer {access_token}"}
            )
        except ConnectionError:
            print("Connection error. Not connection with Spotify servers. ")
            return {}

        if resp.status_code == 200:
            resp_json = resp.json()
            return {
                "track_id": resp_json['item']['id'],
                "track_name": resp_json['item']['name'],
                "artists": ", ".join([artist['name'] for artist in resp_json['item']['artists']]),
                "album": resp_json['item']['album']['name'],
                "cover": resp_json['item']['album']['images']
            }
        else:
            print(f"Status code: {resp.status_code}. Something went wrong :(")
            return {}

    @staticmethod
    def swap_image(url: str) -> str:
        name = CACHE_FOLDER + '/' + url.split('/')[-1] + ".jpeg"
        if not exists(name):
            req = requests.get(url)
            if req.status_code == 200:
                with open(name, 'wb') as wf:
                    for ch in req:
                        wf.write(ch)
        return abspath(name)


class TrackInfoShowGui:
    def __init__(self, root, info=None):
        self.root = root
        self.info = info

        self.frame = None
        self.album = None

        self.root.title(TITLE)
        self.root.geometry(APP_GEOMETRY)
        self.root.configure(bg=BG_COLOR)

        self.set_track(info)

    def set_track(self, info):
        self.info = info
        if info:
            if self.frame:
                self.destroy()

            self.album = Label(
                self.root, text=f"Album: {info['album']}", font=(FONT, 9), bg=BG_COLOR, fg=OTHER_TEXT_COLOR)
            self.track = Label(
                self.root, text=f"Track: { info['track_name'] }", font=(FONT, 10), bg=BG_COLOR, fg=MAIN_TEXT_COLOR)
            self.author = Label(
                self.root, text=f"Artists: {info['artists']}", font=(FONT, 9), bg=BG_COLOR, fg=OTHER_TEXT_COLOR)

            cover = SpotifyFuncs.swapImage(info['cover'][0]['url'])
            pill_img = Image.open(cover).resize(COVER_SIZE, Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(pill_img)

            self.frame = Canvas(self.root, height=COVER_SIZE[0], width=COVER_SIZE[1])
            self.image = self.frame.create_image(0, 0, anchor='nw', image=self.img)

            self.album.place(x=140, y=70)
            self.track.place(x=140, y=20)
            self.author.place(x=140, y=45)
            self.frame.place(x=10, y=10)

    def destroy(self):
        self.album.destroy()
        self.track.destroy()
        self.author.destroy()
        self.frame.destroy()


class CoverShowGUI:
    def __init__(self, root, info):
        self.root = root
        self.info = info
        self.frame = None

        self.root.title(TITLE)
        self.root.geometry(f"{HEIGHT}x{WIDTH}+{CS_X}+{CS_Y}")
        root.resizable(width=RESIZE_ON, height=RESIZE_ON)
        self.set_image(info)

    def set_image(self, info):
        self.info = info

        if info:
            if self.frame:
                self.frame.destroy()

            cover = SpotifyFuncs.swapImage(info['cover'][0]['url'])

            pill_img = Image.open(cover)
            width, height = pill_img.size
            rat = width / height
            if width > WIDTH:
                width = WIDTH
                height = round(width / rat)
            if height > HEIGHT:
                height = HEIGHT
                width = round(height * rat)

            pill_img = pill_img.resize((height, width), Image.ANTIALIAS)

            self.img = ImageTk.PhotoImage(pill_img)

            self.frame = Canvas(self.root, height=HEIGHT, width=WIDTH)
            self.image = self.frame.create_image(0, 0, anchor='nw', image=self.img)

            self.root.geometry(f"{height}x{width}")
            self.frame.pack()


def GUIThread():
    def cycle():
        global track_info
        nonlocal root, TI

        try:
            if track_info != TI.info:
                TI.set_track(track_info)
                CS.set_image(track_info)
        except:
            pass

        root.after(1000, cycle)

    global track_info

    root = Tk()
    sub = Toplevel(root)

    track_info = track_info
    TI = TrackInfoShowGui(root, track_info)
    CS = CoverShowGUI(sub, track_info)

    root.after(1000, cycle)
    root.mainloop()


if __name__ == "__main__":
    track_info = SpotifyFuncs.get_current_track()

    threadGUI = Thread(target=GUIThread, daemon=True)
    threadGUI.isDaemon()
    threadGUI.start()

    while 1:
        track_info = SpotifyFuncs.get_current_track()
        sleep(5)
