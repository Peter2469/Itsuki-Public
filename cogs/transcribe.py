import discord
from discord.ext import commands
import speech_recognition as sr
r = sr.Recognizer()
import os
import random
import io

class transcribeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#This has not been started/nor completed
#It has been kept for no good reason

    @commands.command()
    async def transcribe(self, ctx):
        message = ctx.message
        
        def language(m):
            return m.author == message.author and m.channel == message.channel

        embed=discord.Embed(title="Transcriber", description="Please can you give me the URL of the video/audio you want transcribed, You can attach a file also")
        await ctx.send(embed=embed)

        language = await self.bot.wait_for("message", check=language)

        for att in message.attachments:
            try:
                os.popen(str(f'youtube-dl -i --extract-audio --audio-format flac "{att.proxy_url}"')).read()
                
                chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*().,?0123456789'

                passwords=[]

                for pwd in range(1):
                    password=""
                for c in range(12):
                    password+=random.choice(chars)
                passwords.append(password)
                code = password

                for file in os.listdir("./"):
                    if file.endswith(".flac"):
                        os.rename(file, f'{code}.flac')

                files = sr.AudioFile(f'{code}.flac')

            except Exception as e:
                await ctx.send(e)

        try:
            os.popen(str(f'youtube-dl -i --extract-audio --audio-format flac "{language.content}"')).read()
                    
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*().,?0123456789'

            passwords=[]

            for pwd in range(1):
                password=""
            for c in range(12):
                password+=random.choice(chars)
            passwords.append(password)
            code = password

            for file in os.listdir("./"):
                if file.endswith(".flac"):
                    os.rename(file, f'{code}.flac')

            files = sr.AudioFile(f'{code}.flac')

            with files as source:
                audio = r.record(source)

                if len(r.recognize_sphinx(audio)) > 2000:
                    fp = io.BytesIO(f"{r.recognize_sphinx(audio)}".encode('utf-8'))

                    embed=discord.Embed(title="Transcribed", description=f"Text in Attached File")
                    await ctx.send(embed=embed, file=discord.File(fp, f'{code}.txt'))
                    os.remove(f"{code}.flac")

                else:
                    embed=discord.Embed(title="Transcribed", description=f"{r.recognize_sphinx(audio)}")
                    await ctx.send(embed=embed, file=discord.File(fp, f'{code}.txt'))
                    os.remove(f"{code}.flac")

                    


        except Exception as e:
            await ctx.send(e)



def setup(bot):
    bot.add_cog(transcribeCog(bot))

    