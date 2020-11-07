import discord
from discord.ext import commands
import random


# James's work
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


# Joseph's random stuff
@client.event
async def on_message(message):
    if message.content.startswith('!based'):
        embedVar = discord.Embed(
            title="BASED", description="based_test", color=0x61ff33)
        embedVar.add_field(name="check_f1", value="Yes", inline=False)
        embedVar.add_field(name="check_f2", value="Very Based", inline=False)
        await message.channel.send(embed=embedVar)
