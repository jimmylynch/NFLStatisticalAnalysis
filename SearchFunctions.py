import requests
import time

class SearchFunctions:
    def __init__(self):
        self.playerNameCache = {}
        self.teamNameCache = {}
        url = "https://api.sportradar.com/nfl/official/trial/v7/en/league/teams.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        teamlist = response.json()
        for team in teamlist["teams"]:
            self.teamNameCache[team["name"]] = team["id"]
        self.teamNameCache.pop("TBD")

    def playerFinder(self, name="name", playerid="id"):
        if name != "name":
            if name in self.playerNameCache:
                url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + self.playerNameCache[name] + "/profile.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

                headers = {"accept": "application/json"}

                response = requests.get(url, headers=headers)

                return response.json()
            else:
                for team in self.teamNameCache:
                    print(team)
                    #time.sleep(1)
                    teamid = self.teamNameCache[team]
                    url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + teamid + "/full_roster.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

                    headers = {"accept": "application/json"}

                    response = requests.get(url, headers=headers)
                    teamData = response.json()
                    if 'message' in teamData:
                        return "Retrival Error"

                    for player in teamData["players"]:
                        if player["name"] == name:
                            time.sleep(.5)
                            self.playerNameCache[name] = player["id"]
                            url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + player["id"] + "/profile.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

                            headers = {"accept": "application/json"}

                            response = requests.get(url, headers=headers)
                            return response.json()
                return "No Player Found."

        elif playerid != "id":
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/11cad59d-90dd-449c-a839-dddaba4fe16c/profile.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

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
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + self.teamNameCache[name] + "/profile.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            teamData = response.json()
            if 'message' in teamData:
                return "Retrival Error"
            return teamData
        elif teamid != "id":
            url = "https://api.sportradar.com/nfl/official/trial/v7/en/teams/" + teamid + "/profile.json?api_key=Fkl04nxtzF1ATYAqI0O9z1IwWXnieHna1RQEFsjL"

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            teamData = response.json()
            if 'message' in teamData:
                return "Retrival Error"
            return teamData
        else:
            return "No Team Found."
