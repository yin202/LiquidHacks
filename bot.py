import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import random


# Token from Discord Developer Website
TOKEN = 'Nzc0NDY1NDUwMzM5MDc0MDc5.X6YLKA.CEd15xcXw7BrMxd0Ij6vX1MOIKE'
client = commands.Bot(command_prefix = "!")
# Determines if bot is active or not
@client.event
async def on_ready():
    print('LoL Workout Bot is ready!')


# List of exercises
listExercises = ["squats", "lunges", "high_knees", "plank_rotations", "plank_hold", "wall_sit", 
        "jumping_jacks", "ab_crunches", "pushups", "elbow_planks", "leg_raises", "superman_stretches", 
        "burpees", "jump_squats", "bicycle_crunches", "mountain_climbers", "rest", "run", "flutter_kicks", 
        "box_jumps", "wrist_workout"]


#Champion List Loop (To help with runtime, don't move this pls yet)
lol_watcher = LolWatcher('RGAPI-d121ef6b-adab-4d13-8831-a10fb9ae71fe')
latest = lol_watcher.data_dragon.versions_for_region('na1')['n']['champion']
static_champ_list = lol_watcher.data_dragon.champions(latest, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

userStats = []


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


# Information on the last match
@client.command()
async def work(client, *message):
    if (len(message) < 2):
        if (len(message) == 1):
            regionName = ['br1', 'eun1', 'euw1', 'la1', 'la2',
                          'na1', 'oce', 'oc1', 'ru1', 'tr1', 'jp1', 'kr', 'pbe']
            if message[0].lower() in regionName:
                await client.send("Include a summoner name.")
            else:
                await client.send("Include a region.")
        else:
            await client.send("Enter one region and one summoner name.")
        return
    await client.send("Processing info :thinking:...")
    buildMatchList(message[0], message[1])   # Builds match tables for last 7 matches
    # await firstGameStats(client, *message)
    await client.send(buildMatchList(message[0], message[1])[0])    # Sends the first match table to the client


# Champ Lookup command
@client.command()
async def champLookup(client, *message):
    champName = champ_dict[message[0]]
    print(champ_dict)
    embedVar = discord.Embed(
        title="Champion Lookup", description="Returns the Champion based off of ID", color=0x61ff33)
    embedVar.add_field(name="Champion Name", value=champName, inline=False)
    embedVar.add_field(name="Champion ID", value=message, inline=False)
    await client.send(embed=embedVar)


# DM the author to give help
@client.command()
async def dm(ctx):
    await ctx.author.send("Hello")


# Test command
@client.command()
async def testBML(client, *message):
    await client.send(buildMatchList('sorairo', 'na1')[1])

# DO NOT REMOVE
# get stats for first game
# @client.command()
# async def firstGameStats(client, *message):
#     embedVar = discord.Embed(
#         title="Stats", description="Last Game's Stats", color=0x61ff33)
#     embedVar.add_field(name="Summoner ID", value=userStats[0]['userName'], inline=False)
#     embedVar.add_field(name="Champion", value=userStats[0]['Champion'], inline=False)
#     embedVar.add_field(name="Kills", value=userStats[0]['Kills'], inline=False)
#     embedVar.add_field(name="Deaths", value=userStats[0]['Deaths'], inline=False)
#     embedVar.add_field(name="Assists", value=userStats[0]['Assists'], inline=False)
#     embedVar.add_field(name="Enemy Team Kills", value=userStats[0]['eTeamKills'], inline=False)
#     embedVar.add_field(name="Role", value=userStats[0]['Role'], inline=False)
#     embedVar.add_field(name="Game Length (minutes)", value=userStats[0]['gameLength'], inline=False)
#     embedVar.add_field(name="CS/M", value=userStats[0]['CSM'], inline=False)
#     embedVar.add_field(name="Win?", value=userStats[0]['Win'], inline=False)
#     embedVar.add_field(name="Turrets Destroyed", value=userStats[0]['turretsDestroyed'], inline=False)
#     embedVar.add_field(name="First Baron?", value=userStats[0]['firstBaron'], inline=False)
#     embedVar.add_field(name="First Dragon?", value=userStats[0]['firstDragon'], inline=False)
#     await client.send(embed=embedVar)



###################################################################################################
# 
# RIOT API Helper Functions
#
###################################################################################################
def champLookupInternal(id):
    champName = champ_dict[str(id)]
    return champName


def buildMatchList(user_region, username):
    user = lol_watcher.summoner.by_name(user_region, username)

    match_list = lol_watcher.match.matchlist_by_account(
        user_region, user['accountId'])

    listOfMatches = []
    listOfMatchesDict = []
    userMatchIds = []
    for i in range(0, 7):
        tempMatch = match_list['matches'][i]
        userMatchIds.append(tempMatch['gameId'])
        match_details = lol_watcher.match.by_id(
            user_region, tempMatch['gameId'])
        participants = []
        for row in match_details['participants']:
            participants_row = {}
            findUser = getUsername(match_details['participantIdentities'], row['participantId'])
            participants_row['userName'] = findUser
            if findUser.lower() == username.lower():
                userStats.append(getStats(match_details, findUser, row['participantId'], row['teamId'],
                                          champLookupInternal(row['championId'])))
            participants_row['participantId'] = row['participantId']
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
            # print(match_details['participantIdentities'])
        df = pd.DataFrame(participants)
        listOfMatchesDict.append(participants)
        listOfMatches.append(df)
    return listOfMatches


def getUsername(participantIdentities, participantId):
    for people in participantIdentities:
        if participantId == people['participantId']:
            return (people['player']['summonerName'])
    # print("participant id:")
    # print(participantId)


def getStats(match, userName, participantId, teamId, champ):
    # Role
    role = match['participants'][participantId - 1]['timeline']['role']
    # Enemy Team kills:
    enemyKills = 0
    if (participantId <= 5):
        for x in match['participants']:
            if x['teamId'] == 200:
                enemyKills = x['stats']['kills'] + enemyKills
    else:
        for x in match['participants']:
            if x['teamId'] == 100:
                enemyKills = x['stats']['kills'] + enemyKills

    # Player Deaths
    deaths = match['participants'][participantId - 1]['stats']['deaths']

    # Player Kills
    kills = match['participants'][participantId - 1]['stats']['kills']

    # Player Assists
    assists = match['participants'][participantId - 1]['stats']['assists']

    # Game Duration (seconds)
    gameDuration = match['gameDuration'] / 60

    # Player CSM
    csm = (match['participants'][participantId - 1]['stats']['totalMinionsKilled'] +
           match['participants'][participantId - 1]['stats']['neutralMinionsKilled']) / gameDuration


    # Win/Loss
    if (100 == teamId):
        userWon = match['teams'][0]["win"]
        if userWon == 'Fail':
            userWon = False
        else:
            userWon = True
    else:
        userWon = match['teams'][1]["win"]
        if userWon == 'Fail':
            userWon = False
        else:
            userWon = True

    # Turrets that Player Destroyed
    turretsDestroyed = match['participants'][participantId - 1]['stats']['turretKills']

    # First Baron Status
    if (100 == teamId):
        firstBaron = match['teams'][0]["firstBaron"]
    else:
        firstBaron = match['teams'][1]["firstBaron"]

    # First Dragon Status
    if (100 == teamId):
        firstDragon = match['teams'][0]["firstDragon"]
    else:
        firstDragon = match['teams'][1]["firstDragon"]

    statDesc = {"userName": userName, "Champion": champ,
                "Kills": kills, "Deaths": deaths, "Assists": assists, "eTeamKills": enemyKills, "Role": role,
                "gameLength": gameDuration,
                "CSM": csm, "Win": userWon, "turretsDestroyed": turretsDestroyed, "firstBaron": firstBaron,
                "firstDragon": firstDragon}
    return statDesc


def getStatsAsList():
    return userStats


client.run(TOKEN)
