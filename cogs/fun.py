import discord
from discord.ext import commands
import io
from random import randint
import random
from bs4 import BeautifulSoup
import urllib
import asyncio
import time
import secret
from utils.request import request as req
from utils.request import advrequest as advreq

person = []

class funCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, userName: discord.User, *, message = None):

        if message is None:
            response = await req('https://nekos.life/api/v2/img/hug', "url")
            embed = discord.Embed(title= f'{ctx.author.name}' " hugged " + f'{userName.name}', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

        else:
            response = req('https://nekos.life/api/v2/img/hug', "url")
            embed = discord.Embed(title= f'{ctx.author.name}' " hugged " + f'{userName.name}', description=f"{message}", color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

    @commands.command()
    async def cuddle(self, ctx, userName: discord.User, *, message = None):
        if message is None:
            response = await req('https://nekos.life/api/v2/img/cuddle', "url")
            if response == "https://cdn.nekos.life/cuddle/cuddle_013.gif":
                await ctx.send("This image is NSFW")
            else:
                embed = discord.Embed(title= f'{ctx.author.name}' " cuddled " + f'{userName.name}', color=discord.Color(randint(0x0, 0xFFFFFF)))
                embed.set_image(url=(f"{response}"))
                await ctx.send(embed = embed)

        else:
            response = await req('https://nekos.life/api/v2/img/cuddle', "url")
            if response == "https://cdn.nekos.life/cuddle/cuddle_013.gif":
                await ctx.send("This image is NSFW")
            else:
                embed = discord.Embed(title= f'{ctx.author.name}' " cuddled " + f'{userName.name}', description=f"{message}", color=discord.Color(randint(0x0, 0xFFFFFF)))
                embed.set_image(url=(f"{response}"))
                await ctx.send(embed = embed)

    @commands.command()
    async def kiss(self, ctx, userName: discord.User, *, message = None):

        if message is None:
            response = await req('https://nekos.life/api/v2/img/kiss', "url")
            embed = discord.Embed(title= f'{ctx.author.name}' " kissed " + f'{userName.name}', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

        else:
            response = await req('https://nekos.life/api/v2/img/kiss', "url")
            embed = discord.Embed(title= f'{ctx.author.name}' " kissed " + f'{userName.name}', description=f"{message}", color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

    @commands.command()
    async def slap(self, ctx, userName: discord.User, *, message = None):

        if message is None:
            response = await req('https://nekos.life/api/v2/img/slap', "url")
            embed = discord.Embed(title= f'{ctx.author.name}' " slapped " + f'{userName.name}', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

        else:
            response = await req('https://nekos.life/api/v2/img/slap', "url")
            embed = discord.Embed(title= f'{ctx.author.name} slapped  '+ f'{userName.name}', description=f"{message}", color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

    @commands.command()
    async def pat(self, ctx, userName: discord.User, *, message = None):

        if message is None:
            response = await req('https://nekos.life/api/v2/img/pat', "url")
            embed = discord.Embed(title= f'{ctx.author.name}' " patted " + f'{userName.name}', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

        else:
            response = await req('https://nekos.life/api/v2/img/pat', "url")
            embed = discord.Embed(title= f'{ctx.author.name} patted  '+ f'{userName.name}', description=f"{message}", color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_image(url=(f"{response}"))
            await ctx.send(embed = embed)

    @commands.command()
    async def cat(self, ctx):

        response = await req('http://aws.random.cat/meow', 'file')
        embed = discord.Embed(title= "Here is a cat :cat:", color=discord.Color(randint(0x0, 0xFFFFFF)))
        embed.set_image(url=(f'{response}'))
        await ctx.send(embed = embed)

    @commands.command()
    async def dog(self, ctx):

        response = await req('https://dog.ceo/api/breeds/image/random', 'message')
        embed = discord.Embed(title= "Here is a dog :dog:", color=discord.Color(randint(0x0, 0xFFFFFF)))
        embed.set_image(url=(f'{response}'))
        await ctx.send(embed = embed)

    @commands.command()
    async def compliment(self, ctx, user: discord.User = None):

        if user is None:
            response = await req('https://complimentr.com/api', "compliment")
            embed = discord.Embed(title="", description=(f'{response}'), color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed = embed)
        else:
            response = await req('https://complimentr.com/api', "compliment")
            embed = discord.Embed(title="", description=(f"{user.name } " + f'{response}'), color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed = embed)

    @commands.command(name = "8ball")
    async def eightball(self, ctx, question):

        choice = random.choice(['Maybe.', 'Lol no.', 'Not in your wildest dreams.', 'There is a good chance.', 'Quite Likely.', 'I hope not.', 'I hope so.', 'Hell to the no.', 'No.', 'Possibly.', 'Yes!',
                                'Fuck No', 'Certainly So', 'Unable to answer', 'Sorry, did not quite catch that, please try again later!', 'Denied', 'Granted',
                                'Really that?', 'Affirmative', 'Indeed', 'Okay Dokie', 'Roger that', 'Never!', "Fuck off No!", 'Oh Yes baby', 'No Way', '*Triggered*'])
        embed=discord.Embed(title= "", description= "The 8ball says " + "**" + choice + "**", color=discord.Color(randint(0x0, 0xFFFFFF)))
        await ctx.send(embed = embed)

    @commands.command(aliases=["inspire", "inspireme"])
    async def inspiro(self, ctx):

        f = await req(secret.inspire, None)
        e = discord.Embed(color=discord.Color(randint(0x0, 0xFFFFFF)))
        e.set_image(url=f'{f}')
        await ctx.send(embed=e)

    @commands.command()
    async def chat(self,ctx,*,message):
        async with ctx.typing():
            response = await req(f"https://some-random-api.ml/chatbot?message={message}", "response")
            embed=discord.Embed(title="",description="🤖: "+"**"+ f'{response}' +"**", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @commands.command()
    async def lyrics(self,ctx,*,message):
        async def requesting(data):
            return await req(f"https://some-random-api.ml/lyrics?title={message}", data)

        response = await requesting("lyrics")
        title = await requesting("title")
        thumbnail = await advreq(f"https://some-random-api.ml/lyrics?title={message}", "thumbnail", None, "genius")
        if len(f'{response}') > 2000:
            a = len(f'{response}')
            fp = io.BytesIO(f'{response}'.encode('utf-8'))
            await ctx.send('I can only send lyrics into the channel if it is less then 2000 characters however the lyrics for ' + f'{title}' + " was " + f"**{a}** characters long", file=discord.File(fp, f'{title}'+'.txt'))
        else:
            embed=discord.Embed(title=f'{title}',description=f'{response}', color=discord.Color(randint(0x0, 0xFFFFFF)))
            embed.set_thumbnail(url=f'{thumbnail}')
            await ctx.send(embed=embed)

    @commands.command()
    async def anime(self, ctx, *, anime):
        async def requesting(data, number, data2):
            return await advreq(f"https://api.jikan.moe/v3/search/anime?q={anime}&limit=1", data, number, data2)

        title = await requesting("results", 0, "title")
        url = await requesting("results", 0, "url")
        image_url = await requesting("results", 0, "image_url")
        typequery = await requesting("results", 0, "type")   
        episodes = await requesting("results", 0, "episodes")
        start_date = await requesting("results", 0, "start_date")
        end_date = await requesting("results", 0, "end_date")
        score = await requesting("results", 0, "score")
        rating = await requesting("results", 0, "rated")
        description = await requesting("results", 0, "synopsis")

        embed=discord.Embed(title=f"{title}",url=f"{url}", color=discord.Color(randint(0x0, 0xFFFFFF)))
        embed.set_thumbnail(url=f"{image_url}")
        embed.add_field(name="Type",value=f"{typequery}", inline=False)
        embed.add_field(name="Episodes",value=f"{episodes}", inline=False)
        embed.add_field(name="Start Date",value=f"{start_date}")
        embed.add_field(name="End Date",value=f"{end_date}")
        embed.add_field(name="Score",value=f"{score}", inline=False)
        embed.add_field(name="Rating",value=f"{rating}", inline=False)
        embed.add_field(name="Description",value=f"{description}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def ip(self, ctx, ipaddress):
        async def requesting(data):
            try:
                return await req(f"http://ip-api.com/json/{ipaddress}", data)
            except:
                return "None"

        status = await requesting("status")
        query = await requesting("query")
        city = await requesting("city")
        state = await requesting("regionName")
        country = await requesting("country")
        latitude = await requesting("lat")
        longitude = await requesting("lon")
        isp = await requesting("isp")
        timezone = await requesting("timezone")
        zipq = await requesting("zip")

        if f"{status}" == "success":
            embed = discord.Embed(title=f"Here is the information about {ipaddress}", description="", color=0xFFFFF)
            embed.add_field(name="IP", value=f"{query}")
            embed.add_field(name="City", value=f"{city}")
            embed.add_field(name="State", value=f"{state}")
            embed.add_field(name="Country", value=f"{country}")
            embed.add_field(name="Latitude", value=f"{latitude}")
            embed.add_field(name="Longitude", value=f"{longitude}")
            embed.add_field(name="ISP", value=f"{isp}")
            embed.add_field(name="Timezone", value=f"{timezone}")
            embed.add_field(name="zip", value=f"{zipq}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("An error has came up, either your IP address can't be tracked or its not available")

    @commands.command()
    async def guess(self, ctx):

        if ctx.author.id in person:
            await ctx.send('You are already playing a game, please finish that game before starting a new one!')
        else:
            person.append(ctx.author.id)
            message = ctx.message
            embed = discord.Embed(title="Guessing Game", description="Choose a number from 1 - 1000", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)
            guesses = 1
            number = random.randint(1, 1000)
            print(person)
            while True:
                number2 = int(number)

                def numberguess(m):
                    return m.author == message.author and m.channel == message.channel

                numberguess = await self.bot.wait_for("message", check=numberguess)

                try:

                    if numberguess.content == "quit":
                        embed=discord.Embed(title=f"{ctx.author.name} you gave up!", description=f"The answer was **{number}**", color=discord.Color(randint(0x0, 0xFFFFFF)))
                        await ctx.send(embed=embed)
                        person.remove(ctx.author.id)
                        break

                    answer = number2 - int(numberguess.content)

                    if int(answer) == 0:
                        embed=discord.Embed(title=f"{ctx.author.name} you got it right!", description=f"The number was **{number}** and it only took you **{guesses}** tries!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                        embed.set_footer(text="Say quit to leave")
                        await ctx.send(embed=embed)
                        person.remove(ctx.author.id)
                        break

                    if int(answer) <= 0:
                        embed=discord.Embed(title=f"{ctx.author.name} you got it wrong!", description=f"Your guess was to high, try again!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                        embed.set_footer(text="Say quit to leave")
                        await ctx.send(embed=embed)
                        guesses = guesses + 1
                        continue

                    if int(answer) >= 0:
                        embed=discord.Embed(title=f"{ctx.author.name} you got it wrong!", description=f"Your guess was to low, try again!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                        embed.set_footer(text="Say quit to leave")
                        await ctx.send(embed=embed)
                        guesses = guesses + 1
                        continue
                            
                except:
                    await ctx.send("Letters and emojis are not allowed!")  

    @commands.command()
    async def cguess(self, ctx, top:int):

        if ctx.author.id in person:
            a = await ctx.send('You are already playing a game, please finish that game before starting a new one!')
            await asyncio.sleep(5)
            await a.delete()
        else:
            if int(top) >= 1:
                person.append(ctx.author.id)
                message = ctx.message
                embed = discord.Embed(title="Custom Guessing Game", description=f"Choose a number from 1 - {top}", color=discord.Color(randint(0x0, 0xFFFFFF)))
                await ctx.send(embed=embed)
                guesses = 1
                number = random.randint(1, top)

                while True:
                    number2 = int(number)

                    def numberguess(m):
                        return m.author == message.author and m.channel == message.channel

                    numberguess = await self.bot.wait_for("message", check=numberguess)

                    try:

                        if numberguess.content == f"i-cguess {top}":
                            embed=discord.Embed(title=f"{ctx.author.name} you gave up!", description=f"The answer was **{number}**", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            await ctx.send(embed=embed)
                            person.remove(ctx.author.id)
                            break

                        if numberguess.content == "quit":
                            embed=discord.Embed(title=f"{ctx.author.name} you gave up!", description=f"The answer was **{number}**", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            await ctx.send(embed=embed)
                            person.remove(ctx.author.id)
                            break
                        

                        answer = number2 - int(numberguess.content)
                    
                        if int(answer) == 0:
                            embed=discord.Embed(title=f"{ctx.author.name} you got it right!", description=f"The number was **{number}** and it only took you **{guesses}** tries!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            await ctx.send(embed=embed)
                            person.remove(ctx.author.id)
                            break


                        if int(answer) <= 0:
                            embed=discord.Embed(title=f"{ctx.author.name} you got it wrong!", description=f"Your guess was to high, try again!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            embed.set_footer(text="Say quit to leave")
                            a = await ctx.send(embed=embed)
                            guesses = guesses + 1
                            continue

                        if int(answer) >= 0:
                            embed=discord.Embed(title=f"{ctx.author.name} you got it wrong!", description=f"Your guess was to low, try again!", color=discord.Color(randint(0x0, 0xFFFFFF)))
                            embed.set_footer(text="Say quit to leave")
                            a = await ctx.send(embed=embed)
                            guesses = guesses + 1
                            continue
                    
                    except:
                        a = await ctx.send("Letters and emojis are not allowed!")
            else:
                await ctx.send("0 and below is not allowed!")

    @commands.command(pass_context=True)
    async def insult(self, ctx, user:discord.User = None):
        
        if user is None:
            html = urllib.request.urlopen("https://insult.mattbas.org/api/insult.html").read()
            soup = BeautifulSoup(html,"html.parser")
            insult_text = soup.find('h1')
            embed = discord.Embed(title= "", description=f"{insult_text.text}", color = 0xFFFFF)
            await ctx.send(embed = embed)
        else:
            html = urllib.request.urlopen("https://insult.mattbas.org/api/insult.html").read()
            soup = BeautifulSoup(html,"html.parser")
            insult_text = soup.find('h1')
            embed = discord.Embed(title= "", description=f"{user.name }, { insult_text.text}", color = 0xFFFFF)
            await ctx.send(embed = embed)


#--Error Responses--#

    @cguess.error
    async def cguess_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Give me a number", color=discord.Color(randint(0x0, 0xFFFFFF)))   
            await ctx.send(embed=embed)

    @eightball.error
    async def eightball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please tell 8ball a question", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    #@chat.error
    #async def chat_error(self, ctx, error):
        #if isinstance(error, commands.MissingRequiredArgument):
            #embed=discord.Embed(title="You are missing something", description="Please chat with me :c", color=discord.Color(randint(0x0, 0xFFFFFF)))
            #await ctx.send(embed=embed)
    
    @lyrics.error
    async def lyrics_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please tell me a song you want the lyrics for", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

    @anime.error
    async def anime_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing something", description="Please tell me what anime you want to search for~", color=discord.Color(randint(0x0, 0xFFFFFF)))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(funCog(bot))