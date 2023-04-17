
import discord
from discord.ext import commands

from jsonHandler import jsonHand

description = "The most stupid bot for discord server"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!DG", description=description, intents=intents)


@bot.command()
async def _ping(ctx):
    await ctx.send('Я есть Деграчад')

@bot.command()
async def _parse(ctx, File_name: str):
    result = jsonHand(File_name)
    await ctx.send(result)

#@bot.command()
#async def 

bot.run('MTA1MDgxMTk0NTczNDkxMDAxMg.GUSr-u.9F6rQ6tLYkdiTN3Rg2krBc1zmbacpfZXUoE44M')