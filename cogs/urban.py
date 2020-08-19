import discord
from discord.ext import commands
import sys, traceback
import praw
import random
import asyncio
import urbandictionary as ud
import utils.paginator as paginator
from random import randint
from collections import Counter
import json
import os

class Paginator(paginator.EmbedInterface):
    def __init__(self, ctx, pag):
        self.ctx = ctx
        self.p = pag
        super().__init__(self.ctx.bot, self.p, self.ctx.author)

    async def send_pages(self):
        await self.send_to(self.ctx)

class urbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()


    @commands.command()
    async def urban(self, ctx, *, word):

        if ctx.channel.is_nsfw():
            pag = paginator.EmbedPaginator()

            defs = ud.define(f'{word}')

            e = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e.add_field(name=f"{word}", value=f"{defs[0].definition}".replace("[", "").replace("]", ""), inline=False)
                e.add_field(name="Votes", value=f":thumbsup: **{defs[0].upvotes}** | :thumbsdown: **{defs[0].downvotes}**", inline=False)
            except:
                e.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e2 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e2.add_field(name=f"{word}", value=f"{defs[1].definition}".replace("[", "").replace("]", ""), inline=False)
                e2.add_field(name="Votes", value=f":thumbsup: **{defs[1].upvotes}** | :thumbsdown: **{defs[1].downvotes}**", inline=False)
            except:
                e2.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e2.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e3 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e3.add_field(name=f"{word}", value=f"{defs[2].definition}".replace("[", "").replace("]", ""), inline=False)
                e3.add_field(name="Votes", value=f":thumbsup: **{defs[2].upvotes}** | :thumbsdown: **{defs[2].downvotes}**", inline=False)
            except:
                e3.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e3.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e4 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e4.add_field(name=f"{word}", value=f"{defs[2].definition}".replace("[", "").replace("]", ""), inline=False)
                e4.add_field(name="Votes", value=f":thumbsup: **{defs[2].upvotes}** | :thumbsdown: **{defs[2].downvotes}**", inline=False)
            except:
                e4.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e4.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e5 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e5.add_field(name=f"{word}", value=f"{defs[3].definition}".replace("[", "").replace("]", ""), inline=False)
                e5.add_field(name="Votes", value=f":thumbsup: **{defs[3].upvotes}** | :thumbsdown: **{defs[3].downvotes}**", inline=False)
            except:
                e5.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e5.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e6 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e6.add_field(name=f"{word}", value=f"{defs[4].definition}".replace("[", "").replace("]", ""), inline=False)
                e6.add_field(name="Votes", value=f":thumbsup: **{defs[4].upvotes}** | :thumbsdown: **{defs[4].downvotes}**", inline=False)
            except:
                e6.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e6.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e7 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e7.add_field(name=f"{word}", value=f"{defs[5].definition}".replace("[", "").replace("]", ""), inline=False)
                e7.add_field(name="Votes", value=f":thumbsup: **{defs[5].upvotes}** | :thumbsdown: **{defs[5].downvotes}**", inline=False)
            except:
                e7.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e7.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e8 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e8.add_field(name=f"{word}", value=f"{defs[6].definition}".replace("[", "").replace("]", ""), inline=False)
                e8.add_field(name="Votes", value=f":thumbsup: **{defs[6].upvotes}** | :thumbsdown: **{defs[6].downvotes}**", inline=False)
            except:
                e8.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e8.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e9 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e9.add_field(name=f"{word}", value=f"{defs[7].definition}".replace("[", "").replace("]", ""), inline=False)
                e9.add_field(name="Votes", value=f":thumbsup: **{defs[7].upvotes}** | :thumbsdown: **{defs[7].downvotes}**", inline=False)
            except:
                e9.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e9.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            e10 = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            try:
                e10.add_field(name=f"{word}", value=f"{defs[8].definition}".replace("[", "").replace("]", ""), inline=False)
                e10.add_field(name="Votes", value=f":thumbsup: **{defs[8].upvotes}** | :thumbsdown: **{defs[8].downvotes}**", inline=False)
            except:
                e10.add_field(name=f"Error", value=f"No definition".replace("[", "").replace("]", ""), inline=False)
                e10.add_field(name="Votes", value=f":thumbsup: **0** | :thumbsdown: **0**", inline=False)

            pag.add_page(e)
            pag.add_page(e2)
            pag.add_page(e3)
            pag.add_page(e4)
            pag.add_page(e5)
            pag.add_page(e6)
            pag.add_page(e7)
            pag.add_page(e8)
            pag.add_page(e9)
            pag.add_page(e10)

            interface = Paginator(ctx, pag)
            await interface.send_pages()
        else:
            await ctx.send("Urban Dictionary Requires a NSFW channel")

#--Error Responses--#

    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please tell me what you want to search", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(urbanCog(bot))