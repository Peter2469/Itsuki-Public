import discord
import time
import datetime
import youtube_dl
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio, PCMVolumeTransformer, AudioSource
from tinytag import TinyTag
import urllib.request
from bs4 import BeautifulSoup
import requests
import asyncio
import random
from random import randint
import json
from utils.request import request as req

ffmpeg_options = {

    'options': '-vn'

}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
guildQueues = {}

guildPlayers = {}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.uploader = data.get('uploader')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')
        self.like_count = data.get('like_count')
        self.dislike_count = data.get('dislike_count')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class SleepablePlayer:
    def __init__(self):
        self.player = ""
        self.isInterruptSet = False
        self.voiceClient = None

    async def interruptibleSleep(self, duration):
        i = 0
        while i < duration and not self.isInterruptSet:
            await asyncio.sleep(1)
            i += 1
        self.isInterruptSet = False

    def interrupt(self):
        self.isInterruptSet = True
        self.voiceClient.stop()

class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ownerIds = []

    async def getPlaylistLinks(self, url):
        sourceCode = await req(url , None)
        soup = BeautifulSoup(sourceCode, 'html.parser')
        domain = 'https://www.youtube.com'
        playlist = []
        for link in soup.find_all("a", {"dir": "ltr"}):
            href = link.get('href')
            if href.startswith('/watch?'):
                name = link.string.strip()
                #print(link.string.strip())
                link2 = domain + href.split("&list")[0]
                playlist.append("["+ name + "]" + "(" + link2 + ")")
                print(playlist)
        return playlist

    @commands.command(pass_context=True, aliases=['j', 'jo'])
    async def join(self, ctx):

        channel = ctx.message.author.voice.channel
        if not channel:
            embed = discord.Embed(title="Joined Unsuccessfully", description=f"You are not in a voice channel!",
                                  color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)
            return
        try:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                embed = discord.Embed(title="Moved Successfully",
                                      description=f"I have moved from {voice.channel} to {channel}",
                                      color=discord.Color(randint(0x0, 0xFFFFFF)))
                await ctx.send(embed=embed)
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                embed = discord.Embed(title="Joined Successfully", description=f"I have joined {channel}",
                                      color=discord.Color(randint(0x0, 0xFFFFFF)))
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            #embed = discord.Embed(title="Joined Unsuccessfully",
                                  #description=f"I couldn't join {channel}, do I have the permissions to do so?",
                                  #color=discord.Color(randint(0x0, 0xFFFFFF)))
            #await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        try:
            strGuildId = ctx.guild.id

            if not strGuildId in guildPlayers:
                return

            guildPlayers[strGuildId].interrupt()

        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def play(self, ctx, *, url):

        channel = ctx.message.author.voice.channel
        if not channel:
            return
        try:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                if voice.channel == channel:
                    pass
                else:
                    await voice.move_to(channel)
            else:
                voice = await channel.connect()
        except:
            pass
        count = 0
        strGuildId = str(ctx.guild.id)

        guildPlayers[strGuildId] = SleepablePlayer()

        if "playlist" in url:
            await ctx.send("I have detected this is a playlist, please give me some time!")
            if strGuildId in guildQueues:
                start_time = time.time()
                name = await self.getPlaylistLinks(f"{url}")
                #name = self.link.string.strip()
                lenitem = 0

                for item in name:
                    lenitem = lenitem + 1 
                    guildQueues.get(strGuildId).append(item)
                    print(f"{item} has been added to the queue [{lenitem}/100]")

                # guildQueues.get(strGuildId).append(name)
                current_time = time.time()
                difference = int(round(current_time - start_time))
                text = str(datetime.timedelta(seconds=difference))
                embed=discord.Embed(title=f"Finished", description=f"It took {text}!\n{len(guildQueues[strGuildId]-1)} songs is in queue!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                await ctx.send(embed=embed)
            else:
                guildQueues[strGuildId] = []
                start_time = time.time()
                name = await self.getPlaylistLinks(f"{url}")
                lenitem = 0
                # guildQueues.get(strGuildId).append(name)
                for item in name:
                    lenitem = lenitem + 1 
                    guildQueues.get(strGuildId).append(item)
                    print(f"{item} has been added to the queue [{lenitem}/100]")
                current_time = time.time()
                difference = int(round(current_time - start_time))
                text = str(datetime.timedelta(seconds=difference))
                # print("About to create embed")
                # embed=discord.Embed(title=f"Finished", description=f"It took {text}!\n{len(guildQueues[strGuildId]-1)} songs is in queue!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                # print("Created embed, sending now")
                # await ctx.send(embed=embed)
                # print("Sent embed")
        else:
            if strGuildId in guildQueues:
                guildQueues.get(strGuildId).append(url)
                print("Done")

            else:
                guildQueues[strGuildId] = []
                guildQueues.get(strGuildId).append(url)
                print("Created new string")
        while True:
            if len(guildQueues[strGuildId]) != 0:
                # voice = get(self.bot.voice_clients, guild=ctx.guild)
                guildPlayers[strGuildId].player = await YTDLSource.from_url(guildQueues[strGuildId][0], loop=self.bot.loop)
                guildPlayers[strGuildId].voiceClient = ctx.voice_client
                guildPlayers[strGuildId].voiceClient.play(guildPlayers[strGuildId].player, after=lambda e: print('Player error: %s' % e) if e else None)
                try:
                    embed = discord.Embed(title=guildPlayers[strGuildId].player.title + " is now playing", color=discord.Color(randint(0x0, 0xFFFFFF)))
                except:
                    embed = discord.Embed(title="Error Getting Name", color=discord.Color(randint(0x0, 0xFFFFFF)))
                try:
                    embed.add_field(name="Channel", value=guildPlayers[strGuildId].player.uploader)
                except:
                    embed.add_field(name="Channel", value="Error getting Channel")
                try:
                    embed.set_thumbnail(url=guildPlayers[strGuildId].player.thumbnail)
                except:
                    pass
                try:
                    embed.add_field(name="Duration", value=f"{time.strftime('%H:%M:%S', time.gmtime(guildPlayers[strGuildId].player.duration))}")
                except:
                    embed.add_field(name="Duration", value="Error Getting Duration")
                try:
                    embed.add_field(name="Like Count", value="{:,d}".format(guildPlayers[strGuildId].player.like_count))
                except:
                    embed.add_field(name="Like Count", value="Error getting Like Count")
                try:
                    embed.add_field(name="Dislike Count", value="{:,d}".format(guildPlayers[strGuildId].player.dislike_count))
                except:
                    embed.add_field(name="Dislike Count", value="Error getting dislike count")
                try:
                    embed.add_field(name="Next Song", value=guildQueues[strGuildId][1])
                except:
                    embed.add_field(name="Next Song", value="None")
                try:
                    embed.add_field(name="Queue Length", value=str(len(guildQueues[strGuildId])-1))
                except:
                    embed.add_field(name="Queue Length", value="Error getting Queue Length")
                await ctx.send(embed=embed)
                await guildPlayers[strGuildId].interruptibleSleep(guildPlayers[strGuildId].player.duration)
                guildQueues.get(strGuildId).remove(guildQueues.get(strGuildId)[0])
                print("Deleted Song from Queue")

                print("Checking queue and GCing if possible")
                if len(guildQueues.get(strGuildId)) == 0:
                    guildQueues.pop(strGuildId)
                    print("GC should be complete?")

                print("Current guilds with queues:")
                print(guildQueues.keys())

            else:
                print("Queue length is 0")
                if count == 0:
                    #await self.queue(self, ctx, url)
                    count = count + 1
                else:
                    break

        count = 0
        guildPlayers.pop(strGuildId)
        
    @commands.command()
    async def queue(self, ctx, *, url):

        print("Attempting to queue url " + url)

        strGuildId = str(ctx.guild.id)

        print("Guild ID is " + strGuildId)

        if strGuildId in guildQueues:
            guildQueues.get(strGuildId).append(url)

        else:
            guildQueues[strGuildId] = []
            guildQueues.get(strGuildId).append(url)

        await ctx.send(embed=discord.Embed(title="Added song to queue",
                                           description=f"Your song is in queue ({len(guildQueues[strGuildId])-1} in queue)",
                                           color=discord.Color(randint(0x0, 0xFFFFFF))))
        print("Current queue for guild:")
        print(guildQueues.get(strGuildId))

    @commands.command()
    async def stream(self, ctx, *, url):

        channel = ctx.message.author.voice.channel
        if not channel:
            return
        try:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                if voice.channel == channel:
                    pass
                else:
                    await voice.move_to(channel)
            else:
                voice = await channel.connect()
        except:
            pass

        if url == "smooth":
            voice.play(discord.FFmpegPCMAudio(f"http://ice-the.musicradio.com/SmoothUK"))
            voice.volume = 100
            voice.is_playing()

        if url == "classical":
            voice.play(discord.FFmpegPCMAudio(f"http://ice-the.musicradio.com/ClassicFM"))
            voice.volume = 100
            voice.is_playing()

            voice.play(discord.FFmpegPCMAudio(f"{url}"))
            voice.volume = 100
            voice.is_playing()

            await asyncio.sleep(5)

        else:
            voice.play(discord.FFmpegPCMAudio(f"{url}"))
            voice.volume = 100
            voice.is_playing()

    @commands.command()
    async def pause(self, ctx):

        vc = ctx.voice_client
        vc.pause()
        embed = discord.Embed(title="Paused", description="The song has been paused!",
                              color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx):

        vc = ctx.voice_client
        vc.resume()
        embed = discord.Embed(title="Resumed", description="The song has been resumed!",
                              color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)

    @commands.command(aliasis=['disconnect', 'stop'])
    async def leave(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(title="Disconnect", description=f"I have disconnected!",
                                  color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"I couldn't disconnect, am I in a channel?",
                                  color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    # --Error Responses--#

    @stream.error
    async def stream_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="You are missing something", description="Please give me a url to stream",
                                  color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="You are missing something",
                                  description="Please tell me what you want to play or give me a url",
                                  color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(musicCog(bot))
