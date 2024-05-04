import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys

# Get the path to the 'bin' directory
bin_path = os.path.join(os.path.dirname(__file__), 'bin')

# Add the 'bin' directory to the PYTHONPATH
sys.path.append(bin_path)


# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOME_PATH = os.getenv('HOME_PATH')
owner_id = int(os.getenv('OWNER_ID'))
SERVER_ID = int(os.getenv('SERVER_ID'))

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix='!', owner_id=owner_id, intents=intents)

# Load initial extensions
initial_extensions = ['cogs.commands', 'cogs.pingpong', 'cogs.geardetection']


@bot.event
async def on_ready():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)  # Ensure await here
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            print(e)

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Run the bot
bot.run(TOKEN)