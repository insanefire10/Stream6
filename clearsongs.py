import asyncio
import time
import glob
import os


def clear_songs():
    while True:
        time.sleep(3600)
        print("Deleting Songs")
        folder_path = './audiofiles/*'
        files = glob.glob(folder_path)
        for mp3 in files:
            try:
                os.remove(mp3)
            except:
                print(mp3 + " is in use")
