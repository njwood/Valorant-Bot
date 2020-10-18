# Using the Riot API to make a discord bot

import requests
import os
import discord
from dotenv import load_dotenv
import twitter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TWITTER_AUTH = os.getenv('TWITTER_TOKEN')
TWITTER_SECRET = os.getenv('TWITTER_TOKEN_SECRET')
TWITTER_ACCESS = os.getenv('ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

client = discord.Client()

valorantGuns = ["classic", "shorty", "frenzy", "ghost", "sheriff", "stinger", "spectre", "bucky", "judge", "bulldog",
"guardian", "vandal", "phantom", "marshall", "operator", "odin", "ares"]

api = twitter.Api(consumer_key=TWITTER_AUTH,
                  consumer_secret=TWITTER_SECRET,
                  access_token_key=TWITTER_ACCESS,
                  access_token_secret=TWITTER_ACCESS_SECRET)

def getValorantStats(PlayerName, Tag):
    URL = "https://NA.api.pvp.net/val/content/v1/contents"
    print(URL)

def getValorantInfo():
    URL = "https://na.api.riotgames.com/val/content/v1/contents?locale=en-US&api_key=" + AUTH_TOKEN

    response = requests.get(URL)
    return response.json()

def getSummonerID(PlayerName):

    # Example Query https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Tokimo?api_key=RGAPI-1eb34a3f-1dcd-470a-ad31-4e65da1d7d45
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + PlayerName + "?api_key=" + AUTH_TOKEN

    print(URL)
    response = requests.get(URL)
    return response.json()

def getSummonerRank(ID):
    URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + "?api_key=" + AUTH_TOKEN
    response = requests.get(URL)
    return response.json()

def getTweet(InputAccount):
    status = api.GetUserTimeline(screen_name=InputAccount)
    return status[0].text

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Calls the riot games API and retrieves the summoner ID and their encrypted ID
    if '!rank' in message.content.lower():
        # Obtains the Summoner ID to be put into the function
        try:
            summonerName = message.content.split(' ', 1)[1]
            responseJSON = getSummonerID(summonerName)
            ID = responseJSON['id']
            leagueID = responseJSON['name']
            ID = str(ID)
            leagueID = str(leagueID)

        except:
            await message.channel.send("Summoner, " + summonerName + " does not exist.")
            return

        try:
            responseJSONRank = getSummonerRank(ID)
            summonerRank = responseJSONRank[0]['rank']
            leagueTier = responseJSONRank[0]['tier']
            lp = responseJSONRank[0]['leaguePoints']
            await message.channel.send("Rank of " + leagueID + " is: " + leagueTier + " " + summonerRank + " " + str(lp) + " LP")
            
        except:
            await message.channel.send(summonerName + " is unranked")
            return

    if(message.content == '!patch'):
        await message.channel.send("Find the patch notes for the recent patch here: https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-1-03/")

    if "!guns" in message.content.lower():

        response = ""
        responseJSON = getValorantInfo()
        gun = message.content.split(' ', 1)[1]
        print(gun)

        try:
            #print("In Try")
            if gun.lower() in valorantGuns:
                #print("Gun Exists")
                #print(len(responseJSON['skins']))
                for i in range(0, len(responseJSON['skins'])):
                    #print("Gun: " + gun, "JSON Value: " + responseJSON['skins'][i]['name'].lower())
                    if gun.lower() in responseJSON['skins'][i]['name'].lower():
                        print(responseJSON['skins'][i]['name'])
                        response = response + ", " + responseJSON['skins'][i]['name']
                        #print("In Second Loop")
            #print("Exit")
            await message.channel.send("Gun skins for: " + gun + " " + response)
            return
        except:
            await message.channel.send("Gun does not exist")

    if "!tweet" in message.content:
        try:
            outputMessage = getTweet("playvalorant")
            print(outputMessage)
            await message.channel.send(outputMessage)
        except:
            outputMessage = getTweet("TokimoGames")
            print(str(outputMessage))
            await message.channel.send("Unable to retrieve tweet")

    if message.content == "!agents":
        response = ""
        responseJSON = getValorantInfo()
        for i in range(0,len(responseJSON['characters'])):
            print(responseJSON['characters'][i]['name'])
            response = response + ", " + responseJSON['characters'][i]['name']
        await message.channel.send(response)

client.run(TOKEN)