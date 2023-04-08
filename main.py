import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=, intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send('Конечно крут')

bot.run('MTA1MDgxMTk0NTczNDkxMDAxMg.GUSr-u.9F6rQ6tLYkdiTN3Rg2krBc1zmbacpfZXUoE44M')