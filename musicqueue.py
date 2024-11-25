import youtubeconv
import discord
import asyncio
import discord
import env

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
        self.lastTextChannel = interaction.channel
        self.audio = None


    def addToQueue(self, musicObj: music):
        self.musicArr.append(musicObj)

    async def queuePlayer(self, interaction, client):
        while(len(self.musicArr) > 0):
            print(len(self.musicArr))
            await self.playSong(self.musicArr[0], interaction, client)
            nu = self.musicArr.pop(0)
            if(len(self.musicArr) == 0):
                await asyncio.sleep(180)
                if(len(self.musicArr) == 0):
                    await self.audio.disconnect()
                    self.audio = None
                    await self.lastTextChannel.send(f'Leaving due to inactivity')
                    return
        
        


    async def playSong(self, musicObj, interaction, client):
        print("Player Funct Started")
        if(interaction.guild.get_member(client.user.id).voice is None):
            audio = await interaction.user.voice.channel.connect()
        else:
            audio = interaction.guild.voice_client
        
        ffmpeg_executable_path = env.ffmpeg_loc
        print(musicObj.song_title)
        source = discord.FFmpegPCMAudio(executable=ffmpeg_executable_path,source=f'./audiofiles/{musicObj.song_id}.mp3')
        vol_level = float(0.17)
        audio_renderer = discord.PCMVolumeTransformer(source, volume=vol_level)
        self.audio = audio
        audio.play(audio_renderer)
        print("Now Playing:", musicObj.song_title, "On", interaction.guild.id)
        while audio.is_playing():
            await asyncio.sleep(3)

def findGuildQueue(serverID, guildQueue):
    for x in guildQueue:
        if(serverID == x.serverID):
            return x
    return None

def checkBanList(requester, arr):
    if requester in arr:
        print('Banned User Found')
        return True
    return False