from config import *
from PIL import ImageTk, Image
from tkinter import Canvas, Label
from SpotifyAPIUsage import ImageSwapper

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

            cover = ImageSwapper.swap(info['cover'][0]['url'])
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
