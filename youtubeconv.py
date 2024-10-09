from yt_dlp import YoutubeDL
from yt_dlp.postprocessor import FFmpegPostProcessor
import os
import asyncio

def convertURLtoID(url):
    if 'youtube.com' in url:
        return url.split('youtube.com/watch?v=')[1]
    elif 'youtu.be' in url:
        return (url.split('youtu.be/')[1]).split('?')[0]

def getMusic(url):
    video_url = url
    video_id = convertURLtoID(url)
    fileCheck = f'./audiofiles/{video_id}.mp3'
    if os.path.exists(fileCheck):
        print('Audio already downloaded, skipping download')
        return
    video_info = YoutubeDL().extract_info(url=video_url, download=False)
    options = {
        'format': 'bestaudio[abr<=128k]',
        'keepvideo': False,
        'outtmpl': f'audiofiles/{video_id}',
        'ffmpeg_location' : './ffmpeg/bin/ffmpeg.exe',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality': '128',
        }],
        'postprocessor_args': [
                '-metadata', 'title=%(title)s',
                '-metadata', 'artist=%(uploader)s',
                '-metadata', 'album=%(playlist)s',
                '-metadata', 'length=%(duration)s'
        ],
    }
    with YoutubeDL(options) as ydl:
        out = ydl.download([video_info['webpage_url']])

def getTitle(url):
    video_url = url
    video_info = YoutubeDL().extract_info(url=video_url, download=False)
    video_title = video_info.get('title', None)
    return video_title

def getThumbail(url):
    video_id = convertURLtoID(url)
    return f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
