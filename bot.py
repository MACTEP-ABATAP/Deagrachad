import discord
import os 
import random
from jsonHandler import jsonHand
from dotenv import load_dotenv
import Views

load_dotenv()  
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} готов деграднуть!")

#@bot.slash_command(name="Добавить реакцию для получения роли к сообщению", description="Добавляет ")
#async def reaction_to_message(ctx, message_id: int, role_id: int, emoji: str):

@bot.slash_command(name="degrachad", description="Позови ДеграЧада")
async def ping(ctx):
    await ctx.send('Я есть Деграчад')

@bot.slash_command(name = "сообщение", description="создаёт сообщение")
async def create_message(ctx, message_text: str):
    await ctx.send(message_text)

@bot.slash_command(name="json_reader", description="прочтёт json файл")
async def parse(ctx, file_name: str):
    result = jsonHand(file_name)
    await ctx.send(result)

@bot.slash_command(name="dice", description = "Кинет многогранник")
async def dice(ctx, d: int):
    result = random.randint(1,d)
    await ctx.send(f"На {d}-граннике выпало {result}")

@bot.slash_command()
async def button(ctx):
    await ctx.send("This is a button!", view=Views.View())

bot.run(os.getenv('TOKEN'))
