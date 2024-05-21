import requests
import time
from api_key import apikey


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

    def playerFinder(self, name="name", playerid="id"):
        if name != "name":
            if name in self.playerStatCache: # If player has already been searched, they are stored in cache
                return self.playerStatCache[name]
            else:
                for team in self.teamNameCache:
                    if team in self.teamRostersCache: # If team as already been loaded, no API call is needed
                        for player in self.teamRostersCache[team]:
                            if name == player["name"]:
                                self.cachePlayer(name, player["id"])
                                return self.playerStatCache[name]
                    else: # Team not yet checked, we must call API to get roster
                        time.sleep(.75)
                        teamid = self.teamNameCache[team]
                        url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + teamid + "/full_roster.json?api_key=" + apikey

                        headers = {"accept": "application/json"}

                        response = requests.get(url, headers=headers)
                        teamData = response.json()
                        self.teamRostersCache[team] = teamData["players"]
                        for player in teamData["players"]:
                            if player["name"] == name:
                                self.cachePlayer(name, player["id"])
                                return self.playerStatCache[name]
                return "No Player Found."

        elif playerid != "id":
            for player in self.playerStatCache:
                if player["id"] == playerid:
                    return self.playerStatCache[player]
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + playerid + "/profile.json?api_key=" + apikey

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            playerData = response.json()
            if 'message' in playerData:
                if playerData['message'] == "Object not found":
                    return "No Player Found."
                else:
                    return "Retrival Error"
            else:
                self.playerStatCache[playerData["name"]] = playerData
                return playerData

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

    def cachePlayer(self, name, id):
        #time.sleep(1)
        url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + id + "/profile.json?api_key=" + apikey

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        self.playerStatCache[name] = response.json()
