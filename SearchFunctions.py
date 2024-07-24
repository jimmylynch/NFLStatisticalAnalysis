import requests
import time
from api_key import apikey
from databasefunctions import *

def cachePlayer(id):
    url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + id + "/profile.json?api_key=" + apikey

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = response.json()
    data["_id"] = data.pop("id")
    return addPost("Playerdata", "Players", data)

def playerFinderbyName(playername):
    cachecheck = findPost("Playerdata", "Players", "name", playername)
    if cachecheck != "fail":
        return cachecheck
    rosters = findPost("Teamdata", "Rosters", "", "")
    for team in rosters:
        for player in team["roster"]:
            if playername == player["name"]:
                cachePlayer(player["id"])
                return findPost("Playerdata", "Players", "_id", player["id"])
    return "No Player Found."

def playerFinderbyID(playerid):
    cachecheck = findPost("Playerdata", "Players", "_id", playerid)
    if cachecheck != "fail":
        return cachecheck
    cachePlayer(playerid)
    return findPost("Playerdata", "Players", "_id", playerid)


def teamFinderbyName(teamname):
    return findPost("Teamdata", "Teams", "name", teamname)

def teamFinderbyID(teamid):
    return findPost("Teamdata", "Teams", "_id", teamid)


def getTeamRoster(teamname):
    data = findPost("Teamdata", "Rosters", "name", teamname)
    return data["roster"]