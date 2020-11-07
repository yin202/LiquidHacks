import discord
from discord.ext import commands

# Token from Discord Developer Website
TOKEN = 'Nzc0NDY1NDUwMzM5MDc0MDc5.X6YLKA.CEd15xcXw7BrMxd0Ij6vX1MOIKE'

client = commands.Bot(command_prefix = "!")

# Determines if bot is active or not
@client.event
async def on_ready():
    print('LoL Workout Bot is ready!')

@client.command()
async def numArgs(client, *arg):
    await client.send('Passed {} number of arguments.'.format(len(arg)))

@client.command()
async def echo(client, *message):
    output = ''
    for word in message:
        output += word
        output += ' '
    await client.send('Echo: {}'.format(output))


client.run(TOKEN)
