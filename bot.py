import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import random
import os
import asyncio


# Token from Discord Developer Website
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client = commands.Bot(command_prefix = "!bb")


# Determines if bot is active or not
@client.event
async def on_ready():
    game = discord.Game("Type !bb for help")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('Blue Buff is ready!')


@client.command()
async def info(client, *message):
    embedVar = discord.Embed(
        title="Blue Buff - Information", description="This bot will create a "
                                             "personalized workout routine "
                                             "based on your previous game performance in League of Legends. "
                                             "If you perform well in your game, the bot will give you a easier workout. If you don't, well then...."
                                             "you might think twice about feeding"
                                             " your laner next time!", color=0xceb888)
    path = 'C:/Users/Kevin Tian/Desktop/BlueBuffEmbed.jpg'
    file = discord.File(path, filename= "BlueBuffEmbed.jpg")
    embedVar.add_field(name="Kevin", value="Sophomore @ Purdue University" +"\n" + "Kevin is Double majoring in Data Science and Statistics", inline=False)
    embedVar.add_field(name="James", value="Sophomore @ Columbia University" +"\n" + "James is Majoring in Computer/Electrical Engineering", inline=False)
    embedVar.add_field(name="Joseph", value="Sophomore @ Purdue University" +"\n" + "Joseph is Majoring in Computer Science", inline=False)
    embedVar.add_field(name="Ahmed", value="Sophomore @ Purdue University" +"\n" + "Ahmed is Majoring in Computer Engineering", inline=False)
    await client.send(file = file, embed=embedVar)


# help command
@client.command()
async def h(client, *message):
    embedVar = discord.Embed(
        title="Blue Buff - Help", description="Commands", color=0x734f96)
    embedVar.add_field(name="!bbcreate <region> <summoner name>",
                       value="Creates an exercise routine",
                       inline=False)
    embedVar.add_field(name="!bbinfo",
                       value="Displays information about the bot and it's creators",
                       inline=False)
    embedVar.add_field(name="!bbcalc",
                       value="Displays formula and weighting used to generate workout",
                       inline=False)
    embedVar.add_field(name="!bbh",
                       value="Displays this page",
                       inline=False)
    await client.send(embed=embedVar)



@client.command()
async def calc(client, *message):
    embedVar = discord.Embed(title="Blue Buff - Calculations", 
        description="How the number of repetitions is calculated.", color=0x734f96)
    embedVar.add_field(name="Initial Stats",
                      value="Winning, First Dragon, First Baron",
                      inline=False)
    embedVar.add_field(name = "What changes the State",
                      value = "Deaths, Assists, CSM, Turrets, Dragons, Barons",
                      inline = False)
    await client.send(embed=embedVar)


#Champion List Loop (To help with runtime, don't move this pls yet)
lol_watcher = LolWatcher('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
latest = lol_watcher.data_dragon.versions_for_region('na1')['n']['champion']
static_champ_list = lol_watcher.data_dragon.champions(latest, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']



# Information on the last match
@client.command()
async def create(client, *message):
    if (len(message) < 2):
        embedVar = discord.Embed(
            title="ERROR!", description="The command syntax is !work <region> <summoner name>",
            color=0xFF0000)
        embedVar.add_field(name="Regions", value= "br1, eun1, euw1, la1, la2,na1, oce, oc1, ru1, tr1, jp1, kr, pbe")

        await client.send(embed=embedVar)
        return
    regions = ['br1', 'eun1', 'euw1', 'la1', 'la2', 'na1', 'oce', 'oc1', 'ru1', 'tr1', 'jp1', 'kr', 'pbe']
    if message[0].lower() not in regions:
        embedVar = discord.Embed(
            title="ERROR!", description="The region you have specified is not valid!",
            color=0xFF0000)
        embedVar.add_field(name="Regions", value="br1, eun1, euw1, la1, la2, na1, oce, oc1, ru1, tr1, jp1, kr, pbe")

        await client.send(embed=embedVar)
        return

    await client.send("Processing info :thinking:...")
    userName = ""
    for i in range(1, len(message)-1):
        userName = userName + message[i] + " "
    userName = userName + message[len(message) - 1]
    try:
        x = buildMatchList(message[0], userName)   # Builds match tables for last 7 matches
        times = generateExerciseTimes(x)
        types = generateExerciseType()
    except (IndexError):
        embedVar = discord.Embed(
            title="ERROR!", description="The summoner name does not exist or has not played a game!",
            color=0xFF0000)
        await client.send(embed=embedVar)

    embedVar = discord.Embed(
        title="Exercise Plan", description="A customized exercise plan based off of your performance last game", color=0x61ff33)
    embedVar.add_field(name="Summoner Name", value=x[0]['userName'], inline=False)
    embedVar.add_field(name="Champion", value=x[0]['Champion'], inline=False)
    kdaString = str(x[0]['Kills']) + "/" + str(x[0]['Deaths']) + "/" + str(x[0]['Assists'])
    embedVar.add_field(name="K/D/A", value=kdaString, inline=False)
    for i in range(0, 7):
        exName = types[i]
        r = random.randrange(0, 7)
        numTimes = round(times[r])
        embedVar.add_field(name=exName, value= "Times: " + str((numTimes)))

    await client.send(embed=embedVar)

def generateExerciseTimes(x):

    winNum = 10
    baronNum = 15
    dragNum = 5
    if x[0]['Win'] == True:
        winNum = 0
    if x[0]['firstBaron'] == True:
        baronNum = 0

    if x[0]['firstDragon'] == True:
        dragNum = 0
    numbers = [x[0]['eTeamKills'], x[0]['Deaths']*(1.5)-x[0]['Kills']*(0.2)-x[0]['Assists']*(0.1),
               10 -x[0]['CSM'], winNum, 11-x[0]['turretsDestroyed'], baronNum, dragNum]

    return numbers


def generateExerciseType():
    listExercises = ["Squats", "Lunges", "High Knees", "Plank Rotations", "Plank Hold", "Wall Sit",
                     "Jumping Jacks", "Ab Crunches", "Push-ups", "Elbow Planks", "Leg Raises", "Superman Stretches",
                     "Burpees", "Jump Squats", "Bicycle Crunches", "Mountain Climbers", "Pull-ups", "Neck Stretch", "Flutter Kicks",
                     "Box Jumps", "Wrist Workout"]
    exercises = []
    for i in range(0, 7):
        r = random.randrange(0, len(listExercises))
        exercises.append(listExercises[r])
    return exercises


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
    userStats = []
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
    return userStats


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

client.run(TOKEN)
