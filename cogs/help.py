import discord
from discord.ext import commands
from random import randint
from bs4 import BeautifulSoup

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
        embed.add_field(name="🎮Fun🎮",value="""
`meme <subreddit>` `urban <query>` `inspiro` `guess`  `cguess <number>` `tts` `8ball` `anime <query>` `lyrics <query>` `cat` `dog` `compliment <mention>` `pat <mention>` `hug <mention>` `cuddle <mention>` `kiss <mention>`""", inline=False)
        embed.add_field(name="⚙Utility⚙",value="""
`avatar` `ping` `invite` `speedtest` `sysinfo` `vote` `botinfo` `serverinfo` `userinfo`""", inline=False)
        embed.add_field(name="Music", value="""
`play <name/url>` `pause` `resume` `join` `leave` `stream <audio url/smooth/classical>` `skip`""", inline=False)
        embed.add_field(name="Moderation",value="""
`kick {mention}` `ban {mention}` `clear {amount}` `unban {id}`""")
        embed.add_field(name="Temp Channels", value="""
`tempchannel <duration> <name>` `tempvchannel <duration> <name>`""", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(helpCog(bot))