import requests
import time
from api_key import apikey


class SearchFunctions:
    def __init__(self):
        self.playerNameCache = {}
        self.teamNameCache = {}
        self.teamRostersCache = {}
        url = "https://api.sportradar.com/nfl/official/trial/v7/en/league/teams.json?api_key=" + apikey

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        teamlist = response.json()
        print(teamlist)
        for team in teamlist["teams"]:
            self.teamNameCache[team["name"]] = team["id"]
        self.teamNameCache.pop("TBD")

    def playerFinder(self, name="name", playerid="id"):
        if name != "name":
            if name in self.playerNameCache:
                url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + self.playerNameCache[name] + "/profile.json?api_key=" + apikey

                headers = {"accept": "application/json"}

                response = requests.get(url, headers=headers)

                return response.json()
            else:
                rosterloaded = False
                for team in self.teamNameCache:
                    print(team)
                    if team in self.teamRostersCache or rosterloaded:
                        for player in self.teamRostersCache[team]:
                            if name == player["name"]:
                                self.cachePlayer(name, player["id"])
                                return player
                    else:
                        teamid = self.teamNameCache[team]
                        url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + teamid + "/full_roster.json?api_key=" + apikey

                        headers = {"accept": "application/json"}

                        response = requests.get(url, headers=headers)
                        teamData = response.json()
                        self.teamRostersCache[team] = teamData["players"]
                        for player in teamData["players"]:
                            if player["name"] == name:
                                time.sleep(1)
                                self.cachePlayer(name, player["id"])
                                url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + player[
                                    "id"] + "/profile.json?api_key=" + apikey

                                headers = {"accept": "application/json"}

                                response = requests.get(url, headers=headers)
                                return response.json()
                return "No Player Found."

        elif playerid != "id":
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/11cad59d-90dd-449c-a839-dddaba4fe16c/profile.json?api_key=" + apikey

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            playerData = response.json()
            if 'message' in playerData:
                if playerData['message'] == "Object not found":
                    return "No Player Found."
            if playerData["name"] in self.playerNameCache:
                return playerData
            else:
                self.playerNameCache[playerData["name"]] = playerData["id"]

    def teamFinder(self, name="name", teamid="id"):
        if name in self.teamNameCache:
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + self.teamNameCache[
                name] + "/profile.json?api_key=" + apikey

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            teamData = response.json()
            if 'message' in teamData:
                return "Retrival Error"
            return teamData
        elif teamid != "id":
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + teamid + "/profile.json?api_key=" + apikey

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            teamData = response.json()
            if 'message' in teamData:
                return "Retrival Error"
            return teamData
        else:
            return "No Team Found."

    def cachePlayer(self, name, id):
        self.playerNameCache[name] = id
