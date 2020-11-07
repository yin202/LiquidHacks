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

# Command for creating text box based on multiple inputs
@client.command()
async def suggest(client, *message):
    embedVar = discord.Embed(title="Suggestion", description="Work out fool", color=0x61ff33)
    for word in message:
        embedVar.add_field(name=word, value=word, inline=False)
    await client.send(embed=embedVar)

# Riot Shiet
@client.command()
async def work(client, *message):
    if (len(message) != 2):
        if (len(message) == 1):
            regionName = ['br1', 'eun1', 'euw1', 'la1', 'la2', 'na1', 'oce', 'oc1', 'ru1', 'tr1', 'jp1', 'kr', 'pbe']
            if message[0].lower() in regionName:
                await client.send("Include a summoner name.")
            else:
                await client.send("Include a region.")
        else:
            await client.send("Enter one region and one summoner name.")
        return

    await client.send("Processing info :thinking:...")
    buildMatchList(message[0], message[1])   # Builds match tables for last 7 matches
    await client.send(buildMatchList(message[0], message[1])[0])    # Sends the first match table to the client

    #champs = df.loc[:, "champion"]
    #embedVar = discord.Embed(
    #    title="Champions", description="Player Champions", color=0x61ff33)
    #for i in champs:
    #    embedVar.add_field(name=i, value=i, inline=False)
    #await client.send(embed=embedVar)


# Champ Lookup command
@client.command()
async def champLookup(client, *message):
    lol_watcher = LolWatcher('RGAPI-d121ef6b-adab-4d13-8831-a10fb9ae71fe')
    latest = lol_watcher.data_dragon.versions_for_region('na1')['n']['champion']
    static_champ_list = lol_watcher.data_dragon.champions(latest, False, 'en_US')
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    champName = champ_dict[message[0]]
    print(champ_dict)
    embedVar = discord.Embed(
        title="Champion Lookup", description="Returns the Champion based off of ID", color=0x61ff33)
    embedVar.add_field(name="Champion Name", value=champName, inline=False)
    embedVar.add_field(name="Champion ID", value=message, inline=False)
    await client.send(embed=embedVar)


@client.command()
async def testBML(client, *message):
    await client.send(buildMatchList('sorairo', 'na1')[1])


def champLookupInternal(id):
    lol_watcher = LolWatcher('RGAPI-d121ef6b-adab-4d13-8831-a10fb9ae71fe')
    latest = lol_watcher.data_dragon.versions_for_region('na1')['n']['champion']
    static_champ_list = lol_watcher.data_dragon.champions(
        latest, False, 'en_US')
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    champName = champ_dict[str(id)]
    return champName


def buildMatchList(user_region, username):
    lol_watcher = LolWatcher('RGAPI-d121ef6b-adab-4d13-8831-a10fb9ae71fe')

    user = lol_watcher.summoner.by_name(user_region, username)

    match_list = lol_watcher.match.matchlist_by_account(
        user_region, user['accountId'])

    listOfMatches = []
    listOfMatchesDict = []

    for i in range(0, 7):
        tempMatch = match_list['matches'][i]
        match_details = lol_watcher.match.by_id(
            user_region, tempMatch['gameId'])
        participants = []
        for row in match_details['participants']:
            participants_row = {}
            participants_row['champion'] = row['championId']
            participants_row['spell1'] = row['spell1Id']
            participants_row['spell2'] = row['spell2Id']
            participants_row['win'] = row['stats']['win']
            participants_row['kills'] = row['stats']['kills']
            participants_row['deaths'] = row['stats']['deaths']
            participants_row['assists'] = row['stats']['assists']
            participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
            participants_row['goldEarned'] = row['stats']['goldEarned']
            participants_row['champLevel'] = row['stats']['champLevel']
            participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
            participants_row['item0'] = row['stats']['item0']
            participants_row['item1'] = row['stats']['item1']
            participants_row['championName'] = champLookupInternal(
                row['championId'])
            participants.append(participants_row)
        df = pd.DataFrame(participants)
        listOfMatchesDict.append(participants)
        listOfMatches.append(df)

    return listOfMatches




client.run(TOKEN)
