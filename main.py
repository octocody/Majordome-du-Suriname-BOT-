# Libs
import discord  # For discord
from discord.ext import commands  # For discord
import logging  # For logging
import random
import requests
import os
import json

# Defining a few things
prefix = os.environ.get("prefix")
bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
bot.config_token = os.environ.get("Token")
logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")
    # Another way to use variables in strings
    print("-----\nLogged in as: {} : {}\n-----\nMy current prefix is: -\n-----".format(bot.user.name, bot.user.id))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Surveille le Suriname ! |-help|"))


@bot.command(name='hi', aliases=['hello'])
async def hi(ctx):
    """
    A simple command which says hi to the author.
    """
    await ctx.send(f"Hi {ctx.author.mention}!")
    # Another way to do this code is (user object).mention
    # await ctx.send(f"Hi <@{ctx.author.id}>!")


@bot.command()
async def echo(ctx, *, message=None):
    """
    A simple command that repeats the users input back to them.
    """
    message = message or "Please provide the message to be repeated."
    await ctx.message.delete()
    await ctx.send(message)


@bot.command()
async def ping(ctx):
    """
    A simple command to get ping of the bot.
    """
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.channel.send(f"My ping is {ping}ms")


@bot.command()
async def user(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.message.author
        pronoun = "Your"
    else:
        pronoun = "Their"
    name = f"{member.name}#{member.discriminator}"
    status = member.status
    joined = member.joined_at
    role = member.top_role
    await ctx.channel.send(
        f"{pronoun} name is {name}. {pronoun} status is {status}. They joined at {joined}. {pronoun} rank is {role}.")


@bot.command()
async def ban(ctx, member: discord.User = None, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself!")
        return
    if reason == None:
        reason = "No reason at all!"
    message = f"You have been banned from {ctx.guild.name} for {reason}!"
    await member.send(message)
    await ctx.guild.ban(member)
    await ctx.channel.send(f"{member} is banned!")


@bot.command()
async def prefix(ctx):
    """
    A simple command to get prefix of the bot
    """
    prefix = bot.command_prefix
    await ctx.channel.send(f"The prefix is : {prefix}")


@bot.command()
async def setprefix(ctx, *, new_prefix=None):
    """
    A simple command to get prefix of the bot
    """
    newprefix = new_prefix or "Please provide the new prefix."
    os.environ["prefix"] = newprefix
    await ctx.channel.send(f"The new prefix is : {newprefix}")


@bot.command()
async def clear(ctx, amount=64):
    await ctx.channel.purge(limit=amount)


@bot.command()
async def searchimg(ctx, *, thing=None):
    """
        A simple command to search an image (works with qwant image
    """
    thing_to_search = thing or "Please type what do you want to search"
    url = "https://api.qwant.com/api/search/images?count=50&q=" + thing_to_search + "&t=images&safesearch=1&locale=fr_FR&uiv=4"
    requestHeaders = {
        'User-Agent': 'Plateauschuhe-bot 0.1'
    }
    imgSearchResults = requests.get(
        url,
        headers=requestHeaders).json()
    imgNum = random.randrange(0, 10)
    imgDict = imgSearchResults["data"]["result"]["items"]
    imgObj = imgDict[imgNum]
    imgUrl = "https:" + imgObj["media_fullsize"]
    await ctx.channel.send(f"Here is your image {ctx.author.mention} \n {imgUrl}")


@bot.command()
async def searchvid(ctx, *, video_to_search=None):
    """
        A simple command to search an video (works with qwant video
    """
    videosrch = video_to_search or "Please type what do you want to search"
    url = "https://api.qwant.com/api/search/videos?count=10&q=" + videosrch + "&t=videos&safesearch=1&locale=fr_FR&uiv=4"
    requestHeaders = {
        'User-Agent': 'Plateauschuhe-bot 0.1'
    }
    vidSearchResults = requests.get(
        url,
        headers=requestHeaders).json()
    vidNum = random.randrange(0, 10)
    vidDict = vidSearchResults["data"]["result"]["items"]
    vidObj = vidDict[vidNum]
    vidUrl = "https:" + vidObj["url"]
    await ctx.channel.send(f"Here is your video {ctx.author.mention} \n {vidUrl}")


@bot.command()
async def searchnews(ctx, *, news_to_search=None):
    """
        A simple command to search news (works with qwant video
    """
    newssrch = news_to_search or "Please type what do you want to search"
    url = "https://api.qwant.com/api/search/videos?count=10&q=" + newssrch + "&t=videos&safesearch=1&locale=fr_FR&uiv=4"
    requestHeaders = {
        'User-Agent': 'Plateauschuhe-bot 0.1'
    }
    newsSearchResults = requests.get(
        url,
        headers=requestHeaders).json()
    newsNum = random.randrange(0, 10)
    newsDict = newsSearchResults["data"]["result"]["items"]
    newsObj = newsDict[newsNum]
    newsUrl = "https:" + newsObj["url"]
    await ctx.channel.send(f"{ctx.author.mention} \n {newsUrl}")


@bot.command()
async def searchshopping(ctx, *, thing_to_shop=None):
    """
        A simple command to search the price of something (works with qwant shopping)
    """
    shopsrch = thing_to_shop or "Please type what do you want to search"
    url = "https://api.qwant.com/api/search/shopping?count=10&q=" + shopsrch + "&t=shopping&safesearch=1&locale=fr_FR&uiv=4"
    requestHeaders = {
        'User-Agent': 'Plateauschuhe-bot 0.1'
    }
    shopSearchResults = requests.get(
        url,
        headers=requestHeaders).json()
    shopNum = random.randrange(0, 10)
    shopDict = shopSearchResults["data"]["result"]["items"]
    shopObj = shopDict[shopNum]
    shopUrl = shopObj["offers"][0]["url"]
    priceObj = shopObj["offers"][0]["finalPrice"]
    titleObj = shopObj["product"]["title"]
    sellerObj = shopObj["offers"][0]["name"]
    currencyObj = shopObj["offers"][0]["priceCurrency"]
    imgObj = "https:" + shopObj["product"]['image']['urlMedium']
    await ctx.channel.send(
        f"{ctx.author.mention} \n Price of {shopsrch}  : {titleObj} is {priceObj} {currencyObj} ,sold by {sellerObj} \n {shopUrl} \n here is an image of it : {imgObj} ")


@bot.command()
async def searchmcplayeruuid(ctx, *, playeruuid_to_search=None):
    """
            A simple command to search a minecraft player
    """
    playeruuistosearch = playeruuid_to_search or "Please type the player you want to search"
    url = "https://api.mojang.com/users/profiles/minecraft/" + playeruuistosearch + "?"
    requestHeaders = {
        'User-Agent': 'Plateauschuhe-bot 0.1'
    }
    plyruuidsearchResults = requests.get(
        url,
        headers=requestHeaders).json()
    plyr_uuid = plyruuidsearchResults["id"]
    plyr_name = plyruuidsearchResults["name"]
    await ctx.channel.send(f" {plyr_name} uuid is {plyr_uuid}")


@bot.command()
async def credits(ctx):
    embed = discord.Embed(title="Credits", description="List of Authors", color=0x00ff00)
    author = "@BaconFlex#5438"
    locness = "@Locness#0031"
    embed.add_field(name="Coding", value=f"{author}", inline=False)
    embed.add_field(name="qwant api code",
                    value=f"code of qwant api taken from {locness} : https://github.com/locness3/plateauschuhe-bot",
                    inline=False)
    await ctx.channel.send(embed=embed)


@bot.command()
async def Help2(ctx):
    embed = discord.Embed(title="Help", description="List commands", color=0x00ff00)
    embed.add_field(name="**Moderation Commands**",
                    value=f"All commands start with -\n `Ban` : Command to ban someone, usage : -ban <user> \n `setprefix` : command to change the prefix of the bot \n")

    await ctx.channel.send(embed=embed)


@bot.command()
async def Invite(ctx):
    """
    Invite this bot to your server
    """

    await ctx.channel.send(
        "Here is your link to invite me : https://discordapp.com/oauth2/authorize?client_id=677893235385040936&permissions=8&scope=bot")

@bot.command()
async def covid(ctx, country=None):

    url_covid = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
    country_srch = country or "Please type a country"
    querystring = {}
    querystring['country'] = country_srch

    headers = {
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
        'x-rapidapi-key': "3daf53ec4bmshf3c0b7d67d233b9p184fa4jsn47db4b6ff190"
    }

    response = requests.request("GET", url_covid, headers=headers, params=querystring)
    response_data = response.json()
    num_results = len(response_data['data']["covid19Stats"])
    if response_data["message"] == "OK":
        for x in range(num_results):
            num = x
            results = response_data['data']["covid19Stats"]
            province = results[num]["province"]
            country_rslt = results[num]["country"]
            lastUpdate = results[num]["lastUpdate"]
            confirmed = results[num]["confirmed"]
            deaths = results[num]["deaths"]
            recovered = results[num]["recovered"]
            await ctx.channel.send(f"In {country_rslt} at {province} at{lastUpdate} , The number of confirmed cases is {confirmed} , The number of deaths is {deaths} and the number of recovered cases is {recovered}")
    else:
        await ctx.channel.send("Wrong Country , Try again")
bot.run(bot.config_token)  # Runs our bot