import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

# Load environment variables FIRST
load_dotenv()

# Initialize bot with a command prefix (e.g., "!")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load all cogs on startup
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")  # Remove ".py"
        

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await load_cogs()

# Run the bot with your token
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
