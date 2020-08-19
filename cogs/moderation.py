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

class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, userName: discord.User):
        try:
            await ctx.guild.kick(userName)
            embed = discord.Embed(title= "Kicked Successfully!", description= f'{userName.name} has been kicked successfully!', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_thumbnail(url=userName.avatar_url)
            await ctx.send(embed = embed)
        except:
            embed=discord.Embed(title="Error",description="I was not able to kick them successfully!", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, userName: discord.User):
        try:
            await ctx.guild.ban(userName)
            embed = discord.Embed(title= "Banned Successfully!", description= f'{userName.name} has been banned successfully!', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_thumbnail(url=userName.avatar_url)
            await ctx.send(embed = embed)
        except:
            embed=discord.Embed(title="Error",description="I was not able to ban them successfully!", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command(aliasis=["purge"])
    @commands.has_permissions(kick_members=True)
    async def clear(self,ctx,amount:int):

        try:
            amount2 = int(amount) + 1
            await ctx.channel.purge(limit=amount2)
            embed = discord.Embed(title= "", description= f'**{amount}** message(s)' + " has been deleted successfully!", color=discord.Color(randint(0x0, 0xFFFFFF)))
            yeet = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await yeet.delete()
        except:
            embed=discord.Embed(title="Error",description="I was not able to clear successfully!", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unban(self,ctx,id:int):

        try:
            user = await self.bot.fetch_user(id)
            await ctx.guild.unban(user)
            embed = discord.Embed(title= "Unbanned Successfully!", description= f'{user.name} was unbanned successfully!'
                                , color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed = embed)
        except:
            embed=discord.Embed(title="Error",description="I couldn't unban them successfully!", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)  

#--Error Responses--#
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title="No >:(", description="You dont have permission", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title="No >:(", description="You dont have permission", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title="No >:(", description="You dont have permission", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title="No >:(", description="You dont have permission", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(moderationCog(bot))