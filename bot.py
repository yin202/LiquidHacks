import discord
from discord.ext import commands

# Token from Discord Developer Website
TOKEN = 'Nzc0NDY1NDUwMzM5MDc0MDc5.X6YLKA.CEd15xcXw7BrMxd0Ij6vX1MOIKE'

client = commands.Bot(command_prefix = "!")

# Determines if bot is active or not
@client.event
async def on_ready():
    print('LoL Workout Bot is ready!')

# Simple command to check number of arguments passed


@client.command()
async def numArgs(client, *arg):
    await client.send('Passed {} number of arguments.'.format(len(arg)))

# Simple command to echo a message


@client.command()
async def echo(client, *message):
    output = ''
    for word in message:
        output += word
        output += ' '
    await client.send('Echo: {}'.format(output))


# Command to display text box
@client.event
async def on_message(message):
    if message.content.startswith('!based'):
        embedVar = discord.Embed(
            title="BASED", description="based_test", color=0x61ff33)
        embedVar.add_field(name="check_f1", value="Yes", inline=False)
        embedVar.add_field(name="check_f2", value="Very Based", inline=False)
        await message.channel.send(embed=embedVar)

# Text box with multiple input text
@client.command
async def suggest(client, *message):
    embedVar = discord.Embed(
        title="Suggested Workout", description="What you should do", color=0x61ff33)
    for word in message:
        embedVar.add_field(name=word, value="Do this", inline=False)
    await client.send(embed=embedVar)


client.run(TOKEN)
