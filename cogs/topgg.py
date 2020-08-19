import dbl
import discord
from discord.ext import commands
import secret


class topgg(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = f'{secret.topgg}'
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) 
        

def setup(bot):
    bot.add_cog(topgg(bot))