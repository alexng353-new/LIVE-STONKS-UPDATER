import discord, asyncio, random, configparser, datetime, time
from discord.ext import commands
from discord.ext.commands import Bot
from yahoo_fin import stock_info as yahoo


# Discord Embed Format/Example
@bot.group()
async def embed(ctx):
    e = discord.Embed(title=f"${stockName.upper()} is ${price}", description=phrase, color=stonkChange)
    e.set_image(url=image)
    await ctx.send(embed=embedVar)