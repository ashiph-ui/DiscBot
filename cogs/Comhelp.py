from discord.ext import commands
import discord

class Comhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #help command
    @commands.command()
    async def comhelp(self, ctx):
        embed2 = discord.Embed(title="Commands", description="Here are the avaliable commands",color=discord.Color.red())
        embed2.add_field(name="!hello", value="Greets the user", inline=False)
        embed2.add_field(name="!poll <\"question\">", value="Creates a poll with Yes/No options", inline=False)
        embed2.add_field(name="!roll <min> <max>", value="Rolls a random number between min and max", inline=False)
        embed2.add_field(name="!pickgame <game> <game>...", value="Picks a game out of the options you give.", inline=False)
        embed2.add_field(name="!addstreamer <streamer>", value="adds a streamer for the B-A-B data base and notifys you when online", inline=False)
        embed2.add_field(name="!removestreamer <streamer>", value="removes a streamer from the B-A-B data base", inline=False)
        embed2.add_field(name="!startblackjack", value="starts a blackjack game", inline=False)
        embed2.add_field(name="!hit", value="adds another card to your hand(blackjack)", inline=False)
        embed2.add_field(name="!stand", value="reveals the bots last card(blackjack)", inline=False)
        await ctx.send(embed=embed2)

async def setup(bot):
        await bot.add_cog(Comhelp(bot))