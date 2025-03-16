import os
import discord
from discord.ext import commands, tasks
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitch API endpoints
TWITCH_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
TWITCH_STREAMS_URL = 'https://api.twitch.tv/helix/streams'

class TwitchNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.streamers = {}  # Store streamers and their live status
        self.check_streamers.start()  # Start the background task

    def cog_unload(self):
        self.check_streamers.cancel()  # Stop the background task when the cog is unloaded

    def get_twitch_token(self):
        """Get an access token from the Twitch API."""
        params = {
            'client_id': os.getenv('TWITCH_CLIENT_ID'),
            'client_secret': os.getenv('TWITCH_CLIENT_SECRET'),
            'grant_type': 'client_credentials'
        }
        response = requests.post(TWITCH_TOKEN_URL, params=params)
        return response.json().get('access_token')

    def is_streamer_live(self, streamer_name, token):
        """Check if a streamer is currently live."""
        headers = {
            'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
            'Authorization': f'Bearer {token}'
        }
        params = {
            'user_login': streamer_name
        }
        response = requests.get(TWITCH_STREAMS_URL, headers=headers, params=params)
        data = response.json()
        return len(data['data']) > 0

    @commands.command(name='addstreamer')
    async def add_streamer(self, ctx, streamer_name):
        """Add a streamer to the notification list."""
        if streamer_name not in self.streamers:
            self.streamers[streamer_name] = False
            await ctx.send(f'{streamer_name} has been added to the list.')
        else:
            await ctx.send(f'{streamer_name} is already in the list.')

    @commands.command(name='removestreamer')
    async def remove_streamer(self, ctx, streamer_name):
        """Remove a streamer from the notification list."""
        if streamer_name in self.streamers:
            del self.streamers[streamer_name]
            await ctx.send(f'{streamer_name} has been removed from the list.')
        else:
            await ctx.send(f'{streamer_name} is not in the list.')

    @tasks.loop(minutes=1)  # Check every 1 minute
    async def check_streamers(self):
        """Background task to check if streamers are live."""
        token = self.get_twitch_token()
        for streamer in self.streamers:
            if self.is_streamer_live(streamer, token):
                if not self.streamers[streamer]:
                    self.streamers[streamer] = True
                    channel = self.bot.get_channel(1314340188226584718)  # Replace with your channel ID
                    await channel.send(f'@everyone {streamer} is now live! https://twitch.tv/{streamer}')
            else:
                self.streamers[streamer] = False

    @check_streamers.before_loop
    async def before_check_streamers(self):
        """Ensure the bot is ready before starting the background task."""
        await self.bot.wait_until_ready()

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(TwitchNotifier(bot))