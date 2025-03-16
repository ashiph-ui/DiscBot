import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gooffline(self, ctx):
        """Command to make the bot go offline"""
        await self.bot.change_presence(status=discord.Status.offline)
        await ctx.send("Bot is now offline.")

    @commands.command()
    async def goonline(self, ctx):
        """Command to bring the bot back online"""
        await self.bot.change_presence(status=discord.Status.online)
        await ctx.send("Bot is now online.")

# Setup the cog
async def setup(bot):
    await bot.add_cog(Status(bot))

#need to make changed so that the loop created in twitch doesnt keep the bot online
