import discord
from discord.ext import commands
import sys, traceback
import praw
import random
import asyncio
from datetime import datetime
import utils.paginator as paginator
from random import randint
import os
import json
import secret

class Paginator(paginator.EmbedInterface):
    def __init__(self, ctx, pag):
        self.ctx = ctx
        self.p = pag
        super().__init__(self.ctx.bot, self.p, self.ctx.author)

    async def send_pages(self):
        await self.send_to(self.ctx)

class redditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def meme(self, ctx, *, category):

        try:
            catgirls = ['catgirls', 'Catgirls']
            if category in catgirls:
                await ctx.send("This subreddit has NSFW content which doesn't get filtered.")
            else:
                try:
                    e = discord.Embed(title="Loading if this meme is NSFW and shown in a non-NSFW channel please contact my owner asap\nThe memes will automatically be required to be in a NSFW channel if it has a NSFW tag, this means that it is out of our control for the content you will see", color=discord.Color(randint(0x0, 0xFFFFFF)))
                    aaa = await ctx.send(embed=e)
                    reddit = praw.Reddit(client_id=secret.reddit[0],client_secret=secret.reddit[1],user_agent=secret.reddit[2])
                    memes_submissions = reddit.subreddit(f'{category}').hot()
                    post_to_pick = random.randint(1, 20)
                    for i in range(0, post_to_pick):
                        submission = next(x for x in memes_submissions if not x.stickied)
                    await aaa.delete()
                            
                    if submission.over_18:
                        if ctx.channel.is_nsfw():
                            pag = paginator.EmbedPaginator()

                            embed=discord.Embed(title=submission.title, description=f" [Link if image is not shown]({submission.url})" + f"\n\n{submission.selftext}", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            embed.set_image(url=submission.url)
                            embed.set_footer(text=f"Author: {str(submission.author)} | 👍 {submission.score} | 💬 {submission.num_comments}")
                            await ctx.send(embed=embed)
                            
                            for comment in submission.comments:
                                if isinstance(comment, praw.models.Comment):    
                                    formattedComment = discord.Embed(title=f"Comment by {comment.author}", description=f"{comment.body}", color=discord.Color(randint(0x0, 0xFFFFFF)))
                                    pag.add_page(formattedComment)

                            interface = Paginator(ctx, pag)
                            await interface.send_pages()

                        else:
                            embed=discord.Embed(title=submission.title, description="This meme is NSFW, Please can you do it again in a NSFW Channel", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            embed.set_footer(text=f"Author: {str(submission.author)} | 👍 {submission.score} | 💬 {submission.num_comments}")
                            await ctx.send(embed=embed)
                            


                    else:
                        embed=discord.Embed(title=submission.title, description=f" [Link if image is not shown]({submission.url})" + f"\n\n{submission.selftext}", color=discord.Color(randint(0x0, 0xFFFFFF)))
                        embed.set_image(url=submission.url)

                        embed.set_footer(text=f"Author: {str(submission.author)} | 👍 {submission.score} | 💬 {submission.num_comments}")
                        await ctx.send(embed=embed)
                        pag = paginator.EmbedPaginator()
                        for comment in submission.comments:
                            if isinstance(comment, praw.models.Comment):    
                                formattedComment = discord.Embed(title=f"Comment by {comment.author}", description=f"{comment.body}", color=discord.Color(randint(0x0, 0xFFFFFF)))
                                pag.add_page(formattedComment)

                        interface = Paginator(ctx, pag)
                        await interface.send_pages()
                except Exception as e:
                    e=discord.Embed(title="An Error has occured!",description=f"```{e}```")
                    time = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                    e.set_footer(text=time)
                    await self.bot.owner.send(embed=e)
                    await aaa.delete()
                    await asyncio.sleep(5)
                    embed=discord.Embed(title="Error", description="Is this subreddit spelt correctly?", color=discord.Color(randint(0x0, 0xFFFFFF)))
                    await ctx.send(embed=embed)
        except Exception as e:
            e=discord.Embed(title="An Error has occured!",description=f"```{e}```")
            time = datetime.now().strftime('%d-%m-%y %H:%M:%S')
            e.set_footer(text=time)
            await self.bot.owner.send(embed=e)
            embed=discord.Embed(title="Error", description="Is this subreddit spelt correctly?", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

#--Error Responses--#

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please tell me what subreddit you want to view", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(redditCog(bot))