from config import *
from tkinter import Tk, Toplevel
import SpotifyAPIUsage
import TrackInfoShow
import CoverShow
import time

from threading import Thread, Event
from functools import partial

def TrackInfoThread():
    def cycle():
        global track_info, run
        nonlocal root, TI

        if run == 0: return

        try:
            if track_info != TI.info:
                TI.set_track(track_info)
                CS.set_image(track_info)
        except:
            pass

        root.after(1000, cycle)

    global track_info, run

    root = Tk()
    sub = Toplevel(root)

    track_info = track_info
    TI = TrackInfoShow.TrackInfoShowGui(root, track_info)
    CS = CoverShow.CoverShowGUI(sub, track_info)

    def on_closing():
        root.destroy()
        run = 0

    root.protocol("WM_DELETE_WINDOW", on_closing)

    if run == 0: return
    root.after(1000, cycle)
    root.mainloop()

    run = 0


if __name__ == "__main__":
    run = 1
    track_info = SpotifyAPIUsage.get_current_track()

    threadGUI = Thread(target=TrackInfoThread, daemon=True)
    threadGUI.isDaemon()
    threadGUI.start()

    while run:
        track_info = SpotifyAPIUsage.get_current_track()
        time.sleep(5)
