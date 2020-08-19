import discord
from discord.ext import commands
import sys, traceback
import os
import io
import asyncio
from random import randint
from hurry.filesize import size
import time
import datetime
import shutil
import secret
from collections import Counter

class ownerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.stats = Counter()
        self.ownerIds = []


    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    async def run_cmd(self, cmd: str) -> str:
        process = \
            await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        results = await process.communicate()
        return "".join(x.decode("utf-8") for x in results)

    @commands.command()
    async def delme(self,ctx,id):
        if ctx.author.id in self.ownerIds:
            await self.bot.http.delete_message(ctx.channel.id,f'{id}')
            a = await ctx.send("Done")
            await asyncio.sleep(20)
            await a.delete()
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    async def clean(self,ctx):
        if ctx.author.id in self.ownerIds:
            workingDirectory = "./music"
            filesInDirectory = os.listdir(workingDirectory)
            filesMatchingExtension = []
            fileExtensionsToMatch = [".mp3", ".m4a", ".webm"]
            for file in filesInDirectory:
                fileName, fileExtension = os.path.splitext(workingDirectory + "/" +  file)
                if fileExtension in fileExtensionsToMatch:
                    filesMatchingExtension.append(file)
            totalSize = 0
            for file in filesMatchingExtension:
                #print("File: " + file + " Size: " + str(os.path.getsize(workingDirectory + "/" + str(file))) + " Bytes")
                totalSize += os.path.getsize(workingDirectory + "/" + str(file))
                #print("Total size: " + str(totalSize) + " Bytes")
            message = ctx.message
            def choice(m):
                return m.author == message.author and m.channel == message.channel

            embed=discord.Embed(title="Deletion Size",description=f"{size(totalSize)}")
            embed.set_footer(text="Would you like to delete Y/N")
            await ctx.send(embed=embed)
            channel = await self.bot.wait_for("message", check=choice)

            old = len(filesMatchingExtension)

            if channel.content == "Y":
                before = time.monotonic()
                shutil.rmtree("./music")
                os.mkdir("./music")
                after = time.monotonic()
                ping = (after - before) * 1000
                embed = discord.Embed(title="Deletion Successful")
                embed.add_field(name="Amount",value=old)
                embed.add_field(name="Duration", value=f"{ping:.0f}ms")
                await ctx.send(embed=embed)
            
            if channel.content == "N":
                await ctx.send("Cancelled")
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)



    @commands.command()
    async def update(self, ctx):
        if ctx.author.id in self.ownerIds:
            x = await self.run_cmd(f'{secret.email}')
            await ctx.send(f'''```css
{x}```''')
        else:
            embed=discord.Embed(title="No >:(", description="You are not my owner", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)   


    @commands.command()
    async def cmd(self, ctx, *, cmd):
        if ctx.author.id in self.ownerIds:
            cmd = os.popen(str(cmd)).read()
            embed = discord.Embed(title="", description=cmd, color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    async def cmd2(self, ctx):
        if ctx.author.id in self.ownerIds:

            embed = discord.Embed(description=f"Welcome to the terminal {ctx.author.name}.", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

            while True:

                message = ctx.message

                def channel(m):
                    return m.author == message.author and m.channel == message.channel

                channel = await self.bot.wait_for("message", check=channel)
                
                if channel.content == "exit":
                    embed = discord.Embed(description=f"Exiting the terminal {ctx.author.name}.", color=discord.Color(randint(0x0, 0xFFFFFF)))
                    await ctx.send(embed=embed)
                    break
                x = os.popen(f'{channel.content}').read()
                if len(x) > 2000:
                    fp = io.BytesIO(x.encode('utf-8'))
                    await ctx.send('Too long to output...', file=discord.File(fp, 'eval.txt'))
                else:
                    await ctx.send(f'''```{x}```''')
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)


    @commands.command()
    async def load(self, ctx, *, module: str):
        if ctx.author.id in self.ownerIds:
            """Loads a module."""
            try:
                self.bot.load_extension(f'cogs.{module}')
            except Exception as error:
                exc = traceback.format_exc(limit=500)
                e = discord.Embed(
                    title=error.__class__.__name__, 
                    description=exc,
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )
            else:
                e = discord.Embed(
                    title='Success',
                    description=f'Loaded {module}',
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )

            await ctx.send(embed=e)
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    async def unload(self, ctx, *, module: str):
        if ctx.author.id in self.ownerIds:
            """Loads a module."""
            try:
                self.bot.unload_extension(f'cogs.{module}')
            except Exception as error:
                exc = traceback.format_exc(limit=500)
                e = discord.Embed(
                    title=error.__class__.__name__, 
                    description=exc,
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )
            else:
                e = discord.Embed(
                    title='Success',
                    description=f'Unloaded {module}',
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )

            await ctx.send(embed=e)
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx, *, module: str):
        if ctx.author.id in self.ownerIds:
            """Reloads a module."""
            try:
                self.bot.reload_extension(f'cogs.{module}')
            except commands.ExtensionNotLoaded:
                e = discord.Embed(
                    title='Error', 
                    description=f'{module} is not loaded.',
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )
            except Exception as error:
                exc = traceback.format_exc(limit=500)
                e = discord.Embed(
                    title=error.__class__.__name__, 
                    description=exc,
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )
            else:
                e = discord.Embed(
                    title='Success',
                    description=f'Reloaded {module}',
                    color=discord.Color(randint(0x0, 0xFFFFFF))
                )

            await ctx.send(embed=e)
        else:
            embed=discord.Embed(title="No >:(", description="This is an owner command!",color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ownerCog(bot))
