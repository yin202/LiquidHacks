import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import pandas as pd

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

# Command to display simple BASED text box
@client.command()
async def based(client, *message):
    embedVar = discord.Embed(
        title="BASED", description="based_test", color=0x61ff33)
    embedVar.add_field(name="check_f1", value="Yes", inline=False)
    embedVar.add_field(name="check_f2", value="Very Based", inline=False)
    await client.send(embed=embedVar)

@client.command()
async def suggest(client, *message):
    embedVar = discord.Embed(title="Suggestion", description="Work out fool", color=0x61ff33)
    for word in message:
        embedVar.add_field(name=word, value=word, inline=False)
    await client.send(embed=embedVar)


# Riot Shiet
@client.command()
async def work(client, *message):
    lol_watcher = LolWatcher('RGAPI-d121ef6b-adab-4d13-8831-a10fb9ae71fe')

    region = 'na1'

    me = lol_watcher.summoner.by_name(region, 'sorairo')
    print(me)
    ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
    print(ranked_stats)

    match_list = lol_watcher.match.matchlist_by_account(region, me['accountId'])
    entr = []
    for i in range (0,7):
        entr_row = {}
        entr_row['platformId'] = match_list['matches'][i]['platformId']
        entr_row['gameId'] = match_list['matches'][i]['gameId']
        entr_row['champion'] = match_list['matches'][i]['champion']
        entr_row['queue'] = match_list['matches'][i]['queue']
        entr_row['season'] = match_list['matches'][i]['season']
        entr_row['timestamp'] = match_list['matches'][i]['timestamp']
        entr_row['role'] = match_list['matches'][i]['role']
        entr_row['lane'] = match_list['matches'][i]['lane']
        entr.append(entr_row)

    df = pd.DataFrame(entr)
    await client.send(df)

client.run(TOKEN)
