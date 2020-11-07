import discord
from discord.ext import commands

# Token from Discord Developer Website
TOKEN = 'Nzc0NDY1NDUwMzM5MDc0MDc5.X6YLKA.CEd15xcXw7BrMxd0Ij6vX1MOIKE'

clientCom = commands.Bot(command_prefix = "LoLWork")

# Determines if bot is active not
@clientCom.event
async def on_ready():
    print('LoL Workout Bot is ready!')

clientCom.run(TOKEN)
