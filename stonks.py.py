# Requires the 'members' privileged intents

import discord, configparser, time, datetime, asyncio
from discord.ext import commands, tasks
from yahoo_fin import stock_info as yahoo

description = '''Quoter bot

DATA FROM YAHOO FINANCE

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
                    phrase = "MAKIN BANK."
                    stonkChange = 0x00FF00
                else:
                    image = "https://i.imgflip.com/35a1ly.jpg"
                    phrase = "LOSING MONEY."
                    stonkChange = 0xFF0000

                e = discord.Embed(title=f"${stockName.upper()} is ${price}", description=phrase, color=stonkChange)
                e.set_image(url=image)
                await ctx.send(embed=e)

                print(f'${stockName.upper()} is ${price}      Time: {datetime.datetime.now()}\n{phrase}')

                oldPrice = price

            await asyncio.sleep(timer)
    else:
        await ctx.send('NO SPAM BOT FOR U')

stop = "false"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="STONK PRICES"))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

@bot.group()
async def quote(ctx, stockName: str,):
    """Quotes a stock"""
    price = stockPrice(stockName)
    await ctx.send(f'${stockName.upper()} is ${price}\nTime: {datetime.datetime.now()}')

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
async def quoter(ctx, stockName: str, timer: int,):
    """Posts a stock quote after a specified amount of time in seconds"""
    await timedQuoter(ctx, stockName, timer)

@bot.group()
async def test(ctx):
    role = discord.utils.get(ctx.guild.roles, name="god")
    if role in ctx.author.roles:
        await ctx.send(f'You already have the role {role.name}')

parser = configparser.ConfigParser()

parser.read("config.ini")

bot.run(parser['config']['token'])