import youtubeconv
import discord
import asyncio
import discord

class music:
    def __init__(self, url):
        self.song_url = url
        self.song_id = youtubeconv.convertURLtoID(url)
        self.song_thumbail = youtubeconv.getThumbail(url)
        self.song_title = youtubeconv.getTitle(url)
        

class guildQueue:
    def __init__(self, interaction):
        self.musicArr = []
        self.serverID = interaction.guild.id
        self.voice = interaction.user.voice.channel


    def addToQueue(self, musicObj: music):
        self.musicArr.append(musicObj)
        # result = await asyncio.to_thread(youtubeconv.getMusic, music.song_url)

    async def queuePlayer(self, interaction, client):
        while(len(self.musicArr) > 0):
            print(len(self.musicArr))
            await playSong(self.musicArr[0], interaction, client)
            nu = self.musicArr.pop(0)
            
        

    def getGuildQueue(guild, queues):
        if guild not in queues:
            queues[guild] = guildQueue()
        return queues[guild]

async def playSong(musicObj, interaction, client):
    print("Player Funct Started")
    if(interaction.guild.get_member(client.user.id).voice is None):
        audio = await interaction.user.voice.channel.connect()
    else:
        audio = interaction.guild.voice_client
    
    ffmpeg_executable_path = './ffmpeg/bin/ffmpeg.exe'
    print(musicObj.song_title)
    source = discord.FFmpegPCMAudio(executable=ffmpeg_executable_path,source=f'./audiofiles/{musicObj.song_id}.mp3')
    vol_level = float(0.07)
    audio_renderer = discord.PCMVolumeTransformer(source, volume=vol_level)
    audio.play(audio_renderer)
    print("Now Playing:", musicObj.song_title, "On", interaction.guild.id)
    while audio.is_playing():
        await asyncio.sleep(3)

def checkBanList(requester, arr):
    if requester in arr:
        print('Banned User Found')
        return True
    return False