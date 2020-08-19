import discord
from discord.ext import commands
from discord.utils import get
import sys, traceback
import os
import io
import json
import asyncio
from random import randint
from collections import Counter

#This has not been started/nor completed
#It has been kept for no good reason

class farmCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()


    @commands.command()
    async def setup(self, ctx):
        path = f"/Farm/Person/{ctx.author.id}"
        shit = {"Gold": 0,

        "Slot1": "None",
        "Slot1Start": "None",
        "Slot1Finish": "None",

        "Slot2": "None",
        "Slot2Start": "None",
        "Slot2Finish": "None",

        "Slot3": "None",
        "Slot3Start": "None",
        "Slot3Finish": "None",

        "Slot4": "None",
        "Slot4Start": "None",
        "Slot4Finish": "None",

        "Slot5": "None",
        "Slot5Start": "None",
        "Slot5Finish": "None",

        "Slot6": "None",
        "Slot6Start": "None",
        "Slot6Finish": "None",

        "Slot7": "None",
        "Slot7Start": "None",
        "Slot7Finish": "None",

        "Slot8": "None",
        "Slot8Start": "None",
        "Slot8Finish": "None",

        "Slot9": "None",
        "Slot9Start": "None",
        "Slot9Finish": "None"}

        os.makedirs(path)

        acc = open(f'Farm//Person//{ctx.author.id}//Farm.json', "x")
        acc.write(json.dumps(shit, separators = (', ', ' : ')))
        acc.close()

        embed = discord.Embed(title="Setup", description = "Your Farm is ready!",color =  0xFFFFF)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(farmCog(bot))