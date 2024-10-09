import asyncio
import threading
import os
import discord
from youtubeconv import getMusic, getTitle, getThumbail, convertURLtoID
from clearsongs import clear_songs
import nacl
import time
import env

discord_TOKEN = env.discord_key
ffmpeg_executable_path = './ffmpeg/bin/ffmpeg.exe'
deny_list = []
voice = 'NA'


client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)
music_queue = []

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Game(name='the Talk Tuah Podcast'))
    print(client.user, 'is online!')
    
    
@tree.command(name='ping', description='Ping me👅')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey there!')

@tree.command(name='play', description='Play video from Youtube!' )
@discord.app_commands.describe(url='Enter YouTube URL: ')
async def play(interaction: discord.Interaction, url: str):
    global voice
    userReq = str(interaction.user.id)
    if userReq in deny_list:
            print('User found')
            await interaction.response.send_message(f'Nice Try Diddy')
            return
    await interaction.response.send_message(f'**Downloading, please wait...**')
    videoID = convertURLtoID(url)
    videoTitle = getTitle(url)
    videoThumbail = getThumbail(url)
    result = await asyncio.to_thread(getMusic, url)
    await interaction.edit_original_response(content=f'Done! Now Playing **{videoTitle}**\n{videoThumbail}')
    if(interaction.user.voice):
        if(interaction.guild.get_member(client.user.id).voice is None):
            joinChannel = interaction.user.voice.channel
            voice = await joinChannel.connect()
        source = discord.FFmpegPCMAudio(executable=ffmpeg_executable_path,source=f'./audiofiles/{videoID}.mp3')
        vol_level = float(0.07)
        audio_renderer = discord.PCMVolumeTransformer(source, volume=vol_level)
             
        player = voice.play(audio_renderer)
    else:
        print("You must be in vc")

@tree.command(name='stop', description='Stop playing music!')
async def stop(interaction: discord.Interaction):
     global voice
     voice.stop()



clear_task = threading.Thread(target=clear_songs)
clear_task.daemon = True
clear_task.start()
client.run(discord_TOKEN)