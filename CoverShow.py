from config import *
from PIL import ImageTk, Image
from tkinter import Canvas
from SpotifyAPIUsage import ImageSwapper


class CoverShowGUI:
    def __init__(self, root, info):
        self.root = root
        self.info = info
        self.frame = None

        self.root.title(TITLE)
        self.root.geometry(f"{HEIGHT}x{WIDTH}")
        root.resizable(width=RESIZE_ON, height=RESIZE_ON)
        self.set_image(info)

    def set_image(self, info):
        self.info = info

        if info:
            if self.frame:
                self.frame.destroy()

            cover = ImageSwapper.swap(info['cover'][0]['url'])

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
