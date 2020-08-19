from gtts import gTTS
import discord
from discord.ext import commands
from mutagen.mp3 import MP3
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer, AudioSource
import os
from discord.utils import get
from random import randint
import json
import random
from collections import Counter

class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()


    @commands.command()
    async def tts(self, ctx):

        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*().,?0123456789'

        passwords=[]

        for pwd in range(1):
            password=""
        for c in range(12):
            password+=random.choice(chars)
        passwords.append(password)
        code = password

        message = ctx.message

        def language(m):
            return m.author == message.author and m.channel == message.channel

        embed = discord.Embed(description="What language do you want it in?\nIf you don't know the 2 letter country code please look in the text file", color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)
        await ctx.send(file=discord.File('languages.txt'))

        language = await self.bot.wait_for("message", check=language)

        def choice(m):
            return m.author == message.author and m.channel == message.channel

        embed = discord.Embed(description="Please can you tell me what you want to be in tts", color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)

        channel = await self.bot.wait_for("message", check=choice)
        try:
            f=open(f"{channel.content}.txt", "r")
            contents =f.read()

            tts = gTTS(f'{contents}', lang=f"{language.content}")
            a = await ctx.send("Please wait I am converting your text now!")
            tts.save(f'{code}.mp3')
            await a.delete()
            f.close()

            def audio2(m):
                return m.author == message.author and m.channel == message.channel

            embed = discord.Embed(title="Done Converting" ,description="Please can you choose from the choices below\nDo you want to:\n\n1 = Recieve the audios MP3\n2 = Play the audio in a voice channel\n3 = Both", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

            audio = await self.bot.wait_for("message", check=audio2)

            if audio.content == "1":
                await ctx.send(file=discord.File(f'{code}.mp3'))
                await asyncio.sleep(1)
                os.remove(f'{code}.mp3')


            elif audio.content == "2":
                await ctx.send("Please join a Voice Channel which I can join into, I will join you in 5 seconds")
                await asyncio.sleep(5)
                try:
                    voice = get(self.bot.voice_clients, guild=ctx.guild)
                    channel = ctx.message.author.voice.channel
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()

                    voice.play(discord.FFmpegPCMAudio(f'{code}.mp3'))
                    voice.volume = 100
                    voice.is_playing()
                    audio = MP3(f'{code}.mp3')
                    await asyncio.sleep(audio.info.length)
                    await ctx.send("The tts has finished")
                    os.remove(f'{code}.mp3')
                    await voice.disconnect()
                
                except:
                    await ctx.send("You were not in a Voice Channel in time!\nPlease can you do the command again")
                    os.remove(f'{code}.mp3')
            
            elif audio.content == "3":
                await ctx.send("Here is the audio file")
                await ctx.send(file=discord.File(f'{code}.mp3'))

                try:
                    await ctx.send("Please join a Voice Channel which I can join into, I will join you in 5 seconds")
                    await asyncio.sleep(5)
                    voice = get(self.bot.voice_clients, guild=ctx.guild)
                    channel = ctx.message.author.voice.channel
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()

                    voice.play(discord.FFmpegPCMAudio(f'{code}.mp3'))
                    voice.volume = 100
                    voice.is_playing()
                    audio = MP3(f'{code}.mp3')
                    await asyncio.sleep(audio.info.length)
                    await ctx.send("The tts has finished")
                    os.remove(f'{code}.mp3')
                    await voice.disconnect()
                
                except:
                    await ctx.send("You were not in a Voice Channel in time!\nPlease can you do the command again")
                    os.remove(f'{code}.mp3')

        except:

            tts = gTTS(f'{channel.content}', lang=f"{language.content}")
            a = await ctx.send("Please wait I am converting your text now!")
            tts.save(f'{code}.mp3')
            await a.delete()

            def audio2(m):
                return m.author == message.author and m.channel == message.channel

            embed = discord.Embed(title="Done Converting" ,description="Please can you choose from the choices below\nDo you want to:\n\n1 = Recieve the audios MP3\n2 = Play the audio in a voice channel\n3 = Both", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

            audio = await self.bot.wait_for("message", check=audio2)

            if audio.content == "1":
                await ctx.send(file=discord.File(f'{code}.mp3'))
                await asyncio.sleep(1)
                os.remove(f'{code}.mp3')


            elif audio.content == "2":
                await ctx.send("Please join a Voice Channel which I can join into, I will join you in 5 seconds")
                await asyncio.sleep(5)
                try:
                    voice = get(self.bot.voice_clients, guild=ctx.guild)
                    channel = ctx.message.author.voice.channel
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()

                    voice.play(discord.FFmpegPCMAudio(f'{code}.mp3'))
                    voice.volume = 100
                    voice.is_playing()
                    audio = MP3(f'{code}.mp3')
                    await asyncio.sleep(audio.info.length)
                    await ctx.send("The tts has finished")
                    os.remove(f'{code}.mp3')
                    await voice.disconnect()
                
                except:
                    await ctx.send("You were not in a Voice Channel in time!\nPlease can you do the command again")
                    os.remove(f'{code}.mp3')
            
            elif audio.content == "3":
                await ctx.send("Here is the audio file")
                await ctx.send(file=discord.File(f'{code}.mp3'))

                try:
                    await ctx.send("Please join a Voice Channel which I can join into, I will join you in 5 seconds")
                    await asyncio.sleep(5)
                    voice = get(self.bot.voice_clients, guild=ctx.guild)
                    channel = ctx.message.author.voice.channel
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()
                    if voice and voice.is_connected():
                        await voice.move_to(channel)
                    else:
                        voice = await channel.connect()

                    voice.play(discord.FFmpegPCMAudio(f'{code}.mp3'))
                    voice.volume = 100
                    voice.is_playing()
                    audio = MP3(f'{code}.mp3')
                    await asyncio.sleep(audio.info.length)
                    await ctx.send("The tts has finished")
                    os.remove(f'{code}.mp3')
                    await voice.disconnect()
                
                except:
                    await ctx.send("You were not in a Voice Channel in time!\nPlease can you do the command again")
                    os.remove(f'{code}.mp3')

def setup(bot):
    bot.add_cog(tts(bot))