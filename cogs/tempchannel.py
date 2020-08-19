import discord
from discord.ext import commands
from discord.utils import get
import sys, traceback
import os
import io
import asyncio
from random import randint
from utils.duration import duration as dur

class tempchannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def tempchannel(self, ctx, ation, *, name:str):
        guild = ctx.message.guild
        await guild.create_text_channel(f'{name}')
        await ctx.send(f"The channel {name} has been created!")
        s = name.replace(" ","-")
        a = s.lower()
        channel2 = get(guild.channels, name=f'{a}', type=discord.ChannelType.text)
        channel3 = self.bot.get_channel(int(channel2.id))
        await channel3.send(f"Hello, this is a temporary channel which will be deleted in {ation}!")
        newduration = await dur(ation)
        await asyncio.sleep(int(newduration))
        await channel3.delete(reason="Duration has finished.")
        await ctx.send("Duration has finished.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def tempvchannel(self, ctx, ation, *, name:str):

        guild = ctx.message.guild
        await guild.create_voice_channel(f'{name}')
        await ctx.send(f"The channel {name} has been created!")
        s = name.replace(" ","-")
        a = s.lower()
        channel2 = get(guild.channels, name=f'{a}', type=discord.ChannelType.voice)
        channel3 = self.bot.get_channel(int(channel2.id))
        newduration = await dur(ation)
        await asyncio.sleep(int(newduration))
        await channel3.delete(reason="Duration has finished.")
        await ctx.send("Duration has finished.")

#--Error Responses--#

    @tempchannel.error
    async def tempchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please give me the time and the name of the channel", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

    @tempvchannel.error
    async def tempvchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please give me the time and the name of the channel", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(tempchannelCog(bot))