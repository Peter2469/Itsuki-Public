import dbl
import discord
from discord.ext import commands, tasks

import asyncio
import logging

class logCog(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU5NDIxMDUyNzcyMzUyMDAyNiIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY3MTgxODg3fQ.hLLMe5RoF--z52fdS1BPF1sW5gyzrG0QPfGfYc-pIdY' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)

    # The decorator below will work only on discord.py 1.1.0+
    # In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()

            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

        # if you are not using the tasks extension, put the line below

        await asyncio.sleep(1800)

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(logCog(bot))