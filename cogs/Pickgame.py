import discord
from discord.ext import commands
import random

class PickGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_games = ["Minecraft", "Valorant", "Apex Legends", "Fortnite", "CS:GO"]

    @commands.command()
    async def pickgame(self, ctx, *games):
        """Selects a random game from the provided list or defaults."""
        try:
            # Use the provided games or default to the default list
            game_list = list(games) if games else self.default_games
            if not game_list:
                await ctx.send("No games available to choose from!")
                return

            # Select a random game
            selected_game = random.choice(game_list)

            # Create an embed with the selected game as the title
            embed = discord.Embed(
                title=f"🎮 Let's play **{selected_game}**!",
                description=None,  # No description
                color=discord.Color.purple()  # Purple color
            )

            # Send the embed
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(PickGame(bot))
