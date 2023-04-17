import discord
import os 
from jsonHandler import jsonHand

load_dotenv()  
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="Деграчад", description="Позови ДеграЧада")
async def ping(ctx):
    await ctx.send('Я есть Деграчад')


@bot.slash_command(name="Парсер", description="прочтёт json файл")
async def _parse(ctx, File_name: str):
    result = jsonHand(File_name)
    await ctx.send(result)

bot.run(os.getenv('TOKEN'))
