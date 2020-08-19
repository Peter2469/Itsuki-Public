import discord
from discord.ext import commands
import secret
import sys, traceback
import json
import os
import os.path
import random
import asyncio

G = ["i-", "I-"]

bot = commands.Bot(command_prefix=G)
bot.remove_command('help')
initial_extensions = ['cogs.owner', 'cogs.reddit', 'cogs.help',
'cogs.urban','cogs.tts', 'cogs.fun', 'cogs.music',
'cogs.utility', 'cogs.eval', 'cogs.tempchannel','cogs.log',
'cogs.moderation', 'cogs.topgg']
    
if __name__ == '__main__':
    count = 1
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"[Starting: {count}/{len(initial_extensions)}] Loaded up: {extension}")
            count = count + 1
        except Exception as e:
            print(f'[Failed] {extension} could not load!.', file=sys.stderr)
            traceback.print_exc()
            count = count + 1

@bot.event
async def on_ready():
    bot.fetch_offline_members = False
    print(f'[Loaded] Successfully logged in.')
    while True:
        activity = random.choice(['i-help', f'Currently in {len(bot.guilds)} servers!', f'Ping: {round(bot.latency*1000,2)}ms', 'Version 1.25'])
        await bot.change_presence(activity=discord.Game(name=activity))
        await asyncio.sleep(20)

bot.run(secret.token, bot=True, reconnect=True)
