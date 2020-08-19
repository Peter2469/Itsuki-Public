import discord
from discord.ext import commands
import codecs
import aiohttp
from bs4 import BeautifulSoup
from random import randint
import os
import io
import psutil
import platform
import datetime
import time
import json
from collections import Counter
import os

start_time = time.time()

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()


    @commands.command()
    async def vote(self, ctx):

        embed=discord.Embed(title="Vote",description="[Vote for me](https://discordbots.org/bot/594210527723520026/vote)",color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)

    @commands.command()
    async def sysinfo(self,ctx):

        try:
            os, name, version, _, _, _ = platform.uname()
            name2 = name.replace("","")
            version = version.split('-')[0]
            cores = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory()[2]
            disk_percent = psutil.disk_usage('/')[3]
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            running_since = boot_time.strftime("%A %d/%B/%Y %H:%M:%S ")

            embed=discord.Embed(title="System Info",description=f"""
            I am currently running on **{os} version {version}**
            This system is named **{name2}** and has **{cores}** CPU cores
            Current disk_percent is **{disk_percent}** percent
            Current CPU utilization is **{cpu_percent}** percent
            Current memory utilization is **{memory_percent}** percent
            it's running since **{running_since}**
            """,color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)
        except Exception as Error:
            await ctx.send(Error)
        
    @commands.command()
    async def botinfo(self, ctx):

        before = time.monotonic()
        ping_msg = await ctx.send("Pinging...")
        after = time.monotonic()
        ping = (after - before) * 1000
        await ping_msg.delete()

            
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xFFFFF)

        bot_memory_mb = str(round(psutil.Process(os.getpid()).memory_info()[0] / 1024**2, 2)) + ' MB'
        bot_memory_percent = str(round(psutil.Process(os.getpid()).memory_percent(), 2)) + '%'

        embed = discord.Embed(title=f"Itsuki", description="", color=discord.Color(randint(0x0, 0xFFFFFF)))
        embed.set_thumbnail(url=f"")
        embed.add_field(name="Authors", value="")
        embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Bot Users", value=f"{len(list(self.bot.get_all_members()))}")
        embed.add_field(name='Memory Usage', value=bot_memory_percent + ' (' + bot_memory_mb + ')')
        embed.add_field(name='Ping', value=f"{ping:.0f}ms")
        embed.add_field(name='Uptime', value=text)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self,ctx):

        embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
        emoji_count = len(ctx.message.guild.emojis)
        findbots = sum(1 for member in ctx.guild.members if member.bot)
        guild = ctx.message.guild
        embed.set_author(name=str(guild), icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Owner:", value=str(guild.owner))
        embed.add_field(name="Created at:", value=str(guild.created_at.strftime("%d-%m-%Y at %H:%M:%S")))
        embed.add_field(name='Region', value=guild.region)
        embed.add_field(name='Verification Level', value=str(guild.verification_level))
        embed.add_field(name='Number of emotes', value=str(emoji_count))
        embed.add_field(name="Member Count:", value=str(guild.member_count))
        embed.add_field(name="Bot Count", value=findbots, inline=True)
        embed.add_field(name="Role Count:", value=str(len(guild.roles)))
        embed.add_field(name="Channel Count:", value=str(len(guild.channels)))
        embed.add_field(name="TextChannel Count:", value=str(len(guild.text_channels)))
        embed.add_field(name="VoiceChannel Count:", value=str(len(guild.voice_channels)))
        embed.add_field(name="Category Count:", value=str(len(guild.categories)))
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    async def oserverinfo(self,ctx,*,serverasda = None):
        passed = []
        if ctx.author.id in passed:
            if serverasda is None:
                embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
                emoji_count = len(ctx.message.guild.emojis)
                findbots = sum(1 for member in ctx.guild.members if member.bot)
                guild = ctx.message.guild
                embed.set_author(name=str(guild), icon_url=guild.icon_url)
                embed.set_thumbnail(url=guild.icon_url)
                embed.add_field(name="Owner:", value=str(guild.owner))
                embed.add_field(name="Created at:", value=str(guild.created_at.strftime("%d-%m-%Y at %H:%M:%S")))
                embed.add_field(name='Region', value=guild.region)
                embed.add_field(name='Verification Level', value=str(guild.verification_level))
                embed.add_field(name='Number of emotes', value=str(emoji_count))
                embed.add_field(name="Member Count:", value=str(guild.member_count))
                embed.add_field(name="Bot Count", value=findbots, inline=True)
                embed.add_field(name="Role Count:", value=str(len(guild.roles)))
                embed.add_field(name="Channel Count:", value=str(len(guild.channels)))
                embed.add_field(name="TextChannel Count:", value=str(len(guild.text_channels)))
                embed.add_field(name="VoiceChannel Count:", value=str(len(guild.voice_channels)))
                embed.add_field(name="Category Count:", value=str(len(guild.categories)))
                await ctx.message.channel.send(embed=embed)
            else:
                for server in self.bot.guilds:
                    if f'{serverasda}' == server.name:
                        embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
                        emoji_count = len(server.emojis)
                        findbots = sum(1 for member in server.members if member.bot)
                        guild = ctx.message.guild
                        embed.set_author(name=str(server.name), icon_url=server.icon_url)
                        embed.set_thumbnail(url=server.icon_url)
                        embed.add_field(name="Owner:", value=str(server.owner))
                        embed.add_field(name="Created at:", value=str(server.created_at.strftime("%d-%m-%Y at %H:%M:%S")))
                        embed.add_field(name='Region', value=server.region)
                        embed.add_field(name='Verification Level', value=str(server.verification_level))
                        embed.add_field(name='Number of emotes', value=str(emoji_count))
                        embed.add_field(name="Member Count:", value=str(server.member_count))
                        embed.add_field(name="Bot Count", value=findbots, inline=True)
                        embed.add_field(name="Role Count:", value=str(len(server.roles)))
                        embed.add_field(name="Channel Count:", value=str(len(server.channels)))
                        embed.add_field(name="TextChannel Count:", value=str(len(server.text_channels)))
                        embed.add_field(name="VoiceChannel Count:", value=str(len(server.voice_channels)))
                        embed.add_field(name="Category Count:", value=str(len(server.categories)))
                        await ctx.message.channel.send(embed=embed)
                        try:
                            invs = await server.invites()
                            invs = await server.invites()
                            if len(invs) == 0:
                                await ctx.send("There are no active invites currently on the server.")
                            else:
                                await ctx.send("The currently active invites for this server are: " + ", ".join(map(str, invs)))
                        except Exception as e:
                            await ctx.send(f"{e}")
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self,ctx, user: discord.Member = None):

        if user is None:
            embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            role = ctx.author.top_role.name
            if role == "@everyone":
                role = "No Role"
            voice_state = None if not ctx.author.voice else ctx.author.voice.channel
            embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="Name:", value= ctx.author.name)
            embed.add_field(name="Nick:", value= ctx.author.nick)
            embed.add_field(name="ID:", value= ctx.author.id)
            embed.add_field(name="Status:", value= ctx.author.status)
            embed.add_field(name='In Voice:', value=voice_state)
            embed.add_field(name="Highest Role:", value=role)
            embed.add_field(name="Joined:", value= ctx.author.joined_at.__format__("%d-%m-%Y at %H:%M:%S"))
            embed.add_field(name="Created at:", value= ctx.author.created_at.__format__("%d-%m-%Y at %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            role2 = user.top_role.name
            if role2 == "@everyone":
                role2 = "No Role"
            voice_state = None if not user.voice else user.voice.channel
            embed.set_author(name=str(user.name), icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Name:", value= user.name)
            embed.add_field(name="Nick:", value= user.nick)
            embed.add_field(name="ID:", value= user.id)
            embed.add_field(name="Status:", value= user.status)
            embed.add_field(name='In Voice:', value=voice_state)
            embed.add_field(name="Highest Role:", value=role2)
            embed.add_field(name="Joined:", value= user.joined_at.__format__("%d-%m-%Y at %H:%M:%S"))
            embed.add_field(name="Created at:", value= user.created_at.__format__("%d-%m-%Y at %H:%M:%S"))
            await ctx.send(embed=embed)

    @commands.command()
    async def speedtest(self,ctx):

        embed=discord.Embed(title="Please Wait...")
        a = await ctx.send(embed=embed)
        x = os.popen(f'speedtest --simple --share').read() #pip3 install speedtest
        embed=discord.Embed(title="Speedtest",description=f"{x}",color=discord.Color(randint(0x0, 0xFFFFFF)))
        await a.edit(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, user: discord.User = None):

        if user is None:
            embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=ctx.author.avatar_url)
            embed.add_field(
                name="Avatar",
                value=f"[Link]({ctx.author.avatar_url})",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=user.avatar_url)
            embed.add_field(
                name="Avatar",
                value=f"[Link]({user.avatar_url})",
                inline=True,
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):

        embed=discord.Embed(title="Pong!",description=f"{round(self.bot.latency*1000,2)}ms", color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):

        embed=discord.Embed(title="Invite",description=f'[Link](Bot Invite Link Here)', color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(helpCog(bot))