from discord.ext import commands
import discord

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self,ctx, question: str):
        embed = discord.Embed(title=question,description=None, color=discord.Color.purple())
        embed.add_field(name="React with 👍 for Yes", value="React with 👎 for No")
        
        # Send the poll and mention the author
        message = await ctx.send(embed=embed)
        
        # Add reaction options
        await message.add_reaction("👍")
        await message.add_reaction("👎")

async def setup(bot):
        await bot.add_cog(Poll(bot))