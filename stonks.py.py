# Requires the 'members' privileged intents

import discord, configparser, time, datetime, asyncio, os, random
from discord.ext.commands.core import check
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands, tasks
from yahoo_fin import stock_info as yahoo
from PIL import Image

description = '''Quoter bot

DATA FROM YAHOO FINANCE

NOTE: USE SLOWQUOTER FOR STOCKS THAT UPDATE LIVE

Commands:'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', description=description, intents=intents)

def stockPrice(stockName):
    return round(yahoo.get_live_price(stockName), 3)
   
async def timedQuoter(ctx, stockName: str, timer: int,):
    role = discord.utils.get(ctx.guild.roles, name = "god")
    if role in ctx.author.roles:

        price = stockPrice(stockName)
        oldPrice = price

        initialEmbed = discord.Embed(title=f"${stockName.upper()} is ${price}", description=f"Time: {datetime.datetime.now()}", color=0x00FFFF)
        await ctx.send(embed=initialEmbed)

        time.sleep(1)
        while 1:
            price = stockPrice(stockName)
            if price != oldPrice:
                if price > oldPrice:
                    image = "https://i.kym-cdn.com/entries/icons/facebook/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg"
                    phrase1 = "MAKIN BANK."
                    stonkChange = 0x00FF00
                else:
                    image = "https://i.imgflip.com/35a1ly.jpg"
                    phrase1 = "LOSING MONEY."
                    stonkChange = 0xFF0000

                e = discord.Embed(title=f"${stockName.upper()} is ${price}", description=phrase1, color=stonkChange)
                e.set_image(url=image)
                await ctx.send(embed=e)

                print(f'${stockName.upper()} is ${price}      Time: {datetime.datetime.now()}\n{phrase1}')

                oldPrice = price

            await asyncio.sleep(timer)
    else:
        await ctx.send('NO SPAM BOT FOR U')

async def presenceChanger():
    parser = configparser.ConfigParser()
    parser.read("presence.ini")
    
    while 1:
        parser.read("presence.ini")
        count = len(open("presence.ini").readlines())
        number = random.randint(1,count-1)
        presence = parser["presence"][str(number)]

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(presence)))
        await asyncio.sleep(5)

async def imager(status: str, stockName: str, price):
    image2 = Image.open(f'{status}.jpg')
    image3 = Image.open('online.jpg')

    #resize, first image
    image2 = image2.resize((2800, 1600))
    image3 = image3.resize((2800, 1600))
    image3_size = image3.size
    image2_size = image2.size

    new_image = Image.new('RGB',(image3_size[0], 3200), (250,250,250))
    new_image.paste(image3,(0,0))
    new_image.paste(image2,(0,image3_size[1]))
    new_image.save("combined.png","PNG")

stop = "false"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await presenceChanger()

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

@bot.group()
async def quote(ctx, stockName: str,):
    """Quotes a stock"""
    price = stockPrice(stockName)

    e = discord.Embed(title=f"${stockName.upper()} is ${price}", description=f"Time: {datetime.datetime.now()}")

    await ctx.send(embed = e)

@bot.group()
async def fastQuoter(ctx, stockName: str,):
    """Posts when a stock is up or down"""
    timer = 1
    await timedQuoter(ctx, stockName, timer)
    

@bot.group()
async def slowQuoter(ctx, stockName: str,):
    """Posts a quote every 15 seconds to avoid rate limiting"""
    await timedQuoter(ctx, stockName, 15)
    
@bot.group()
async def graph(ctx, stockName: str,):
    """Graph \"stock name\""""
    role = discord.utils.get(ctx.guild.roles, name = "god")
    if role in ctx.author.roles:
             
        plt.ylabel('Price')

        currentstock = []
        price = stockPrice(stockName)
        oldPrice = price
        currentstock.append(round(yahoo.get_live_price(stockName), 3))
        print(currentstock)

        #logger
        f = open(f"{stockName.upper()} {datetime.datetime.now().date()}.txt", "w")
        f.write(f"Logging {stockName.upper()}\nPrice, Time\n")
        f.write(f"{price}, {datetime.datetime.now()}\n")

        plt.plot(currentstock)
        plt.savefig('online.jpg', bbox_inches='tight')

        file = discord.File("online.jpg",filename = "online.jpg")       
        await ctx.send(file = file)

        e = discord.Embed(title=f"Starting Graph for {stockName.upper()}", description=f".stop to stop")
        e.add_field(name="Current price", value=price)
        e.add_field(name="Time:", value=datetime.datetime.now())

        await ctx.send(embed = e) 
        
        global run
        run = True

        while run == True:
            price = stockPrice(stockName)

            if price != oldPrice:

                #Add value to list
                currentstock.append(price)
                f.write(f"{price}, {datetime.datetime.now()}\n")

                if price > oldPrice:
                    await imager("up", stockName, price)
                    stonkChange = 0x00FF00
                    graphColor = "#00FF00"

                else:
                    await imager("down", stockName, price)
                    stonkChange = 0xFF0000
                    graphColor = "#FF0000"

                # Add points to graph, color changes relative to ups and downs.

                plt.plot(currentstock, color = graphColor)
                plt.savefig('online.jpg', bbox_inches='tight')
                
                oldPrice = price
                phrase = f"Graphing **{stockName.upper()}** prices."

                e = discord.Embed(title=f"${stockName.upper()} is ${price}", description=phrase, color=stonkChange)

                file = discord.File("combined.png", filename="image.png")

                e.set_image(url = "attachment://image.png")
                e.add_field(name="Current price", value=f"${str(price)}")
                e.add_field(name="Time:", value=datetime.datetime.now())

                await ctx.send(file=file, embed=e)
                
                print(currentstock)
                
            await asyncio.sleep(2)

        await ctx.send(f"Stopped graphing **{stockName}**")
        print(f"Stopped graphing {stockName}")
        
            
                
    else:
        await ctx.send('NO SPAM BOT FOR U')

@bot.group()
async def quoter(ctx, stockName: str, timer: int,):
    """Posts a stock quote after a specified amount of time in seconds"""
    await timedQuoter(ctx, stockName, timer)

@bot.group()
async def test(ctx):
    role = discord.utils.get(ctx.guild.roles, name="god")
    if role in ctx.author.roles:
        await ctx.send(f'You already have the role {role.name}')

@bot.group()
async def restart(ctx):
    embed = discord.Embed(title="Restarting")
    file = discord.File("die.png", filename="die.png")
    embed.set_image(url="attachment://die.png")
    await ctx.send(file=file, embed=embed)

    os.system("./restart.sh")
    
@bot.group()
async def stop(ctx):
    global run
    run = False

    await ctx.send("**stopping...**")

parser = configparser.ConfigParser()

parser.read("config.ini")

bot.run(parser['config']['token'])
