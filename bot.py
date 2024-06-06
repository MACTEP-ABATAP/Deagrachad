import discord
import os
import random
import logging
import json
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# Загрузка переменных окружения
load_dotenv('secret.env')

# Получение токена из переменной окружения
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("TOKEN not found in environment variables.")
    exit(1)

# Настройка бота с необходимыми намерениями
intents = discord.Intents.default()
intents.message_content = True  # Включение привилегированных намерений
intents.presences = True        # Включение намерения присутствий
intents.members = True          # Включение намерения членов сервера

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)


bot = MyBot()

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

@bot.tree.command(name="degrachad", description="Позови ДеграЧада")
async def degrachad(interaction: discord.Interaction):
    await interaction.response.send_message('Я есть Деграчад')

@bot.tree.command(name="сообщение", description="создаёт сообщение")
async def create_message(interaction: discord.Interaction, message_text: str):
    await interaction.response.send_message(message_text)

@bot.tree.command(name="json_reader", description="прочтёт json файл")
async def parse(interaction: discord.Interaction, file_name: str):
    try:
        with open(file_name, 'r') as file:
            result = json.load(file)
        await interaction.response.send_message(str(result))
    except Exception as e:
        logging.error(f"Error reading JSON file: {e}")
        await interaction.response.send_message("Ошибка при чтении файла.")

@bot.tree.command(name="dice", description="Кинет многогранник")
async def dice(interaction: discord.Interaction, d: int):
    if d <= 0:
        await interaction.response.send_message("Количество граней должно быть больше нуля.")
        return
    result = random.randint(1, d)
    await interaction.response.send_message(f"На {d}-граннике выпало {result}")

@bot.tree.command(name="choose_game", description="Случайным образом выбирает игру с учетом предпочтений")
async def choose_game(interaction: discord.Interaction):
    games = load_games()
    if not games:
        await interaction.response.send_message("Список игр пуст.")
        return

    user_ratings = {}
    for game in games:
        avg_rating = calculate_average_rating(game)
        user_ratings[game["name"]] = avg_rating

    sorted_games = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)
    weighted_games = [game[0] for game in sorted_games for _ in range(int(game[1] * 10))]

    chosen_game = random.choice(weighted_games)
    await interaction.response.send_message(f"Сегодня играем в: {chosen_game}")

@bot.tree.command(name="suggest_game", description="Добавляет игру в список предложений")
async def suggest_game(interaction: discord.Interaction, name: str, genre: str):
    games = load_games()
    games.append({"name": name, "genre": genre, "ratings": {}})
    save_games(games)
    await interaction.response.send_message(f"Игра '{name}' добавлена в список предложений.")

@bot.tree.command(name="rate_game", description="Оцените игру")
async def rate_game(interaction: discord.Interaction, name: str, rating: float):
    games = load_games()
    user = str(interaction.user)

    for game in games:
        if game["name"] == name:
            if "ratings" not in game:
                game["ratings"] = {}
            game["ratings"][user] = rating
            save_games(games)
            await interaction.response.send_message(f"Ваша оценка для '{name}' сохранена!")
            return
    await interaction.response.send_message(f"Игра '{name}' не найдена в списке предложений.")

@bot.tree.command(name="results", description="Показывает результаты голосования")
async def results(interaction: discord.Interaction):
    games = load_games()
    if not games:
        await interaction.response.send_message("Список игр пуст.")
        return
    results_str = "\n".join([f"{game['name']}: {calculate_average_rating(game)} средний рейтинг" for game in games])
    await interaction.response.send_message(f"Результаты голосования:\n{results_str}")

@bot.tree.command(name="schedule", description="Создаёт событие для совместной игры")
async def schedule(interaction: discord.Interaction, date: str, time: str, game: str):
    event_message = f"Запланировано событие:\nИгра: {game}\nДата: {date}\nВремя: {time}"
    await interaction.response.send_message(event_message)

# Запуск бота с токеном из переменной окружения
bot.run(TOKEN)
