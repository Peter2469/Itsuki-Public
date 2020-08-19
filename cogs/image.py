from gtts import gTTS
import discord
from discord.ext import commands
from mutagen.mp3 import MP3
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer, AudioSource
import os
from discord.utils import get
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from collections import Counter

class imageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()


    @commands.command()
    async def fuckoff(self,ctx):
        try:
            url = str(ctx.author.avatar_url).replace("gif","png")
            try:
                resp = requests.get(url, stream=True).raw

            except requests.exceptions.RequestException as e:  
                await ctx.send(e)

            try:
                img2 = Image.open(resp)

            except IOError:
                print("unable to use image")
                    
            new_width  = 75
            new_height = 75

            fontsize = 29
            #fontsize2 = 20

            if len(f"{ctx.author.name} Joined!") >= 19:
                a = len(f"{ctx.author.name} Joined!")
                number = a - 20
                fontsize = 27 - number
            else:
                fontsize = 30

            #if len(f"{ctx.author.name} Joined!") >= 20:
                #a = len(f"{ctx.author.name} Joined!")
                #number = a - 20
                #fontsize2 = 20 - number
            #else:
                #pass

            avatar = img2.resize((new_width, new_height), Image.ANTIALIAS)
            avatar.convert('RGBA')
            avatar.save(f'profile/{ctx.author.id}avatar.png')

            im = Image.open(f'profile/{ctx.author.id}avatar.png')
            bigsize = (im.size[0] * 3, im.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask) 
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(im.size, Image.ANTIALIAS)
            im.putalpha(mask)
            im.convert('RGBA')
            im.save(f'profile/{ctx.author.id}avatar.png')

            backgroundresize=Image.open(f'background.png')
            backgroundresize.convert('RGBA')
            new_width  = 400
            new_height = 150
            backgroundresization = backgroundresize.resize((new_width, new_height), Image.ANTIALIAS)
            backgroundresization.convert('RGBA')
            backgroundresization.save(f'background.png')
            img = Image.open('background.png')
            draw = ImageDraw.Draw(img)
            foreground=Image.open(f'profile/{ctx.author.id}avatar.png')
            font = ImageFont.truetype(f"Fonts/Fug.ttf", fontsize)
            foreground.convert('RGBA')
            img.paste(foreground,(20, 30),foreground)
            draw.text((115, 50), f"{ctx.author.name} Joined!", fill="white", font=font)
            #draw.text((115, 20), f"Server Count:{ctx.guild.member_count} Members!", fill="white", font=font2)
            img.save(f'profile/{ctx.author.id}final.png')
            await ctx.send(file=discord.File(f'profile/{ctx.author.id}final.png'))
        except Exception as e:
            await ctx.send(f"""{e}""")

        

        

def setup(bot):
    bot.add_cog(imageCog(bot))