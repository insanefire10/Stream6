import asyncio
import time


def clear_songs():
    while True:
        time.sleep(300)
        print("Deleting Songs")
        folder_path = './audiofiles'