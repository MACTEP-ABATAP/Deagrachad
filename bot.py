import discord
import os
import random
import logging
import json
from dotenv import load_dotenv
from discord.ext import commands
import Views

load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Настройка логирования
logging.basicConfig(level=logging.INFO)

GAMES_FILE = 'games.json'

def load_games():
    try:
        with open(GAMES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_games(games):
    with open(GAMES_FILE, 'w') as file:
        json.dump(games, file, indent=4)

def calculate_average_rating(game):
    if "ratings" not in game or not game["ratings"]:
        return 0
    return sum(game["ratings"].values()) / len(game["ratings"])

@bot.event
async def on_ready():
    logging.info(f"{bot.user} готов деграднуть!")

@bot.command(name="degrachad", help="Позови ДеграЧада")
async def ping(ctx):
    await ctx.send('Я есть Деграчад')

@bot.command(name="сообщение", help="создаёт сообщение")
async def create_message(ctx, *, message_text: str):
    await ctx.send(message_text)

@bot.command(name="json_reader", help="прочтёт json файл")
async def parse(ctx, file_name: str):
    try:
        with open(file_name, 'r') as file:
            result = json.load(file)
        await ctx.send(str(result))
    except Exception as e:
        logging.error(f"Error reading JSON file: {e}")
        await ctx.send("Ошибка при чтении файла.")

@bot.command(name="dice", help="Кинет многогранник")
async def dice(ctx, d: int):
    if d <= 0:
        await ctx.send("Количество граней должно быть больше нуля.")
        return
    result = random.randint(1, d)
    await ctx.send(f"На {d}-граннике выпало {result}")

@bot.command(name="button", help="Показывает кнопку")
async def button(ctx):
    await ctx.send("This is a button!", view=Views.View())

@bot.command(name="choose_game", help="Случайным образом выбирает игру с учетом предпочтений")
async def choose_game(ctx):
    games = load_games()
    if not games:
        await ctx.send("Список игр пуст.")
        return

    user_ratings = {}
    for game in games:
        avg_rating = calculate_average_rating(game)
        user_ratings[game["name"]] = avg_rating

    sorted_games = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)
    weighted_games = [game[0] for game in sorted_games for _ in range(int(game[1] * 10))]

    chosen_game = random.choice(weighted_games)
    await ctx.send(f"Сегодня играем в: {chosen_game}")

@bot.command(name="suggest_game", help="Добавляет игру в список предложений")
async def suggest_game(ctx, name: str, genre: str):
    games = load_games()
    games.append({"name": name, "genre": genre, "ratings": {}})
    save_games(games)
    await ctx.send(f"Игра '{name}' добавлена в список предложений.")

@bot.command(name="rate_game", help="Оцените игру")
async def rate_game(ctx, name: str, rating: float):
    games = load_games()
    user = str(ctx.author)

    for game in games:
        if game["name"] == name:
            if "ratings" not in game:
                game["ratings"] = {}
            game["ratings"][user] = rating
            save_games(games)
            await ctx.send(f"Ваша оценка для '{name}' сохранена!")
            return
    await ctx.send(f"Игра '{name}' не найдена в списке предложений.")

@bot.command(name="results", help="Показывает результаты голосования")
async def results(ctx):
    games = load_games()
    if not games:
        await ctx.send("Список игр пуст.")
        return
    results_str = "\n".join([f"{game['name']}: {calculate_average_rating(game)} средний рейтинг" for game in games])
    await ctx.send(f"Результаты голосования:\n{results_str}")

@bot.command(name="schedule", help="Создаёт событие для совместной игры")
async def schedule(ctx, date: str, time: str, *, game: str):
    event_message = f"Запланировано событие:\nИгра: {game}\nДата: {date}\nВремя: {time}"
    await ctx.send(event_message)

# Запуск бота с токеном из переменной окружения
bot.run(os.getenv('TOKEN'))
