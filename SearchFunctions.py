import requests
import time
from api_key import apikey
from databasefunctions import *

class SearchFunctions:
    def __init__(self):
        self.playerStatCache = {} # Stores data of each player searched
        self.teamNameCache = {}
        self.teamRostersCache = {}
        url = "https://api.sportradar.com/nfl/official/trial/v7/en/league/teams.json?api_key=" + apikey

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        teamlist = response.json()
        for team in teamlist["teams"]:
            self.teamNameCache[team["name"]] = team["id"]
        self.teamNameCache.pop("TBD")

    def teamFinder(self, name="name", teamid="id"):
        if name != "name":
            if name in self.teamNameCache: # This means a valid name is entered
                if name in self.teamRostersCache: # Returns roster if it was already retrieved
                    return self.teamRostersCache[name]
                url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + self.teamNameCache[name] + "/full_roster.json?api_key=" + apikey

                headers = {"accept": "application/json"}

                response = requests.get(url, headers=headers)

                teamData = response.json()
                if 'message' in teamData:
                    return "Retrival Error"
                self.teamRostersCache[name] = teamData["players"]
                return teamData
            else:
                return "No Team Found."
        elif teamid != "id":
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + teamid + "/full_roster.json?api_key=" + apikey

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)

            teamData = response.json()
            self.teamRostersCache[teamData['name']] = teamData
            if 'message' in teamData:
                return "Retrival Error"
            return teamData
        else:
            return "No Team Found."


def cachePlayer(id):
    url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + id + "/profile.json?api_key=" + apikey

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = response.json()
    data["_id"] = data.pop("id")
    return addPost("Playerdata", "Players", data)

def playerFinder(self, name="name", playerid="id"):
    if name != "name":
        cachecheck = findPost("Playerdata", "Players", "name", name)
        if cachecheck != "fail":
            return cachecheck
        else:
            rosters = findPost("Teamdata", "Rosters", "", "")
            for team in rosters:
                for player in team["roster"]:
                    if name == player["name"]:
                        cachePlayer(player["id"])
                        return findPost("Playerdata", "Players", "_id", player["id"])
            return "No Player Found."

    elif playerid != "id":
        cachecheck = findPost("Playerdata", "Players", "_id", playerid)
        if cachecheck != "fail":
            return cachecheck
        url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + playerid + "/profile.json?api_key=" + apikey

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        playerdata = response.json()

        if 'message' in playerdata:
            if playerdata['message'] == "Object not found":
                return "No Player Found."
            else:
                return "Retrival Error"
        else:
            playerdata["_id"] = playerdata.pop("id")
            addPost("Playerdata", "Players", playerdata)
            return playerdata
