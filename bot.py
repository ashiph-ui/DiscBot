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

@bot.command(name="roll", help="Roll a random number between two values. Usage: !roll [min] [max]")
@commands.cooldown(1, 5, commands.BucketType.user)  # 5-second cooldown per user
async def roll(ctx, min_val: int = 1, max_val: int = 6):
    """
    Roll a random number between min and max (default 1-6)
    Examples:
    !roll       -> Rolls 1-6
    !roll 10    -> Rolls 1-10
    !roll 5 20  -> Rolls 5-20
    """
    # Handle inverted min/max
    if min_val > max_val:
        min_val, max_val = max_val, min_val  # Auto-swap values

    # Generate and send result
    result = random.randint(min_val, max_val)
    await ctx.send(f"🎲 {ctx.author.mention} rolled **{result}** ({min_val}-{max_val})")

@roll.error
async def roll_error(ctx, error):
    """Custom error handler for roll command"""
    if isinstance(error, commands.BadArgument):
        await ctx.send("❌ Please use numbers only! Example: `!roll 1 20`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing arguments! Usage: `{ctx.prefix}roll [min] [max]`\n"
                       "Examples:\n"
                       "- `!roll` (1-6)\n"
                       "- `!roll 10` (1-10)\n"
                       "- `!roll 5 20` (5-20)")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Please wait {error.retry_after:.1f}s before rolling again!")
    else:
        await ctx.send("❌ An unexpected error occurred!")

# Run the bot with your token
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
