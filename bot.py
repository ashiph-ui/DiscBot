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

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

# Command: Respond to "!hello"
@bot.command()
async def hello(ctx):
    await ctx.send(f"I heard, {ctx.author.mention} is gey!")

@bot.command()
async def roll(ctx, min: int, max: int):
    number = random.randint(min, max)
    await ctx.send(f"{ctx.author.mention} rolled a {number}!")

# Run the bot with your token
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
