# Stream6
This is a Python application I created to allow my peers to listen to audio from any YouTube video in Discord voice calls, allowing everyone in the call to listen to a video!

## Add to your server!
`https://discord.com/oauth2/authorize?client_id=1292990437090398218&permissions=551903423488&integration_type=0&scope=bot`

## How it works
* The app listens for a slash command from a text channel in the Discord Server
* A user chooses the command and provides the URL to the YouTube video
* The app provides the user's link to a Youtube MP3 downloader library (yt_dlp) and the library returns an mp3 in the `audiofiles` directory
* The app then opens the newly created MP3 and Discord.py uses FFMPEG to render audio
* The app connects to the voice channel and starts playing the requested audio!

## How to use
* Make sure these Python libraries are installed:
```
discord
yt_dlp
Update if needed: os, asyncio
```

* Open Discord Dev Portal, create an app, and get its bot ID. Open `main.py ` and enter your bot ID
* Download FFMPEG, extract its contents in a folder in the directory. Go back into `main.py` and add change path to the executable
* Open terminal and run `python main.py` and you are done!

## Copyright notice
This application does download audio from YouTube. Please do not use this bot to listen to copyrighted audio as it may violate YouTube Terms of Service. I am not responsible if this bot is used irresponsibly.

## Future plans
* Embed support for a nicer UI
* Pause/Skip functions
* Queue support
