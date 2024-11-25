import asyncio
import threading
import os
import discord
from youtubeconv import getMusic, getTitle, getThumbail, convertURLtoID
from clearsongs import clear_songs
import musicqueue
import nacl
import time
import env

discord_TOKEN = env.discord_key
deny_list = []
voice = 'NA'

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)
guildQueue = []

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='the Talk Tuah Podcast'))
    print(client.user, 'is online!')
    
    
@tree.command(name='ping', description='Ping me👅')
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey there!')

@tree.command(name='play', description='Play video from Youtube!' )
@discord.app_commands.describe(url='Enter YouTube URL: ')
async def play(interaction: discord.Interaction, url: str):
    if musicqueue.checkBanList(str(interaction.user.id), deny_list):
        await interaction.response.send_message(f'Nice Try Diddy')
        return
    if(interaction.user.voice):
        musicContainer = musicqueue.music(url)
    else:
        await interaction.response.send_message(f'You must be in a voice channel to use this!')
        return
    
    await interaction.response.send_message(f'**Downloading, please wait...**')

    serverQueueExists = False
    serverQueue = ""
    for x in guildQueue:
        if(interaction.guild.id == x.serverID):
            serverQueue = x
            serverQueueExists = True
            break
    if(serverQueueExists == False):
        serverQueue = musicqueue.guildQueue(interaction)
        guildQueue.append(serverQueue)

    result = await asyncio.to_thread(getMusic, url)
    printData(guildQueue)

    await interaction.edit_original_response(content=f'Done! Now Playing **{musicContainer.song_title}**\n{musicContainer.song_thumbail}')
    serverQueue.addToQueue(musicContainer)
    if(len(serverQueue.musicArr) == 1):
        await serverQueue.queuePlayer(interaction, client)

@tree.command(name='skip', description='Skip to next song in queue')
async def stop(interaction: discord.Interaction):
    serverQueue = musicqueue.findGuildQueue(interaction.guild.id, guildQueue)
    if(serverQueue is None):
        await interaction.response.send_message("I am not in a voice channel!")
        return
    if(serverQueue.audio is None):
        await interaction.response.send_message("I am currently not playing a song!")
        return
    serverQueue.audio.stop()
    await interaction.response.send_message(f'Skipping')


def printData(allGuilds):
    for x in allGuilds:
        print(x.musicArr)
        print(x.serverID)
        print(x.voice)


clear_task = threading.Thread(target=clear_songs)
clear_task.daemon = True
clear_task.start()
client.run(discord_TOKEN)