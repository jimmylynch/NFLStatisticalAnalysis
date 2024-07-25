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
    addPost("Playerdata", data["position"], data)
    return data


def playerFinderbyName(playername,position = None):
    if position is None: # Base case where we don't know position
        db = cluster["Playerdata"]
        positions = db.list_collection_names()
        for position in positions:
            cachecheck = findPost("Playerdata",position,"name",playername)
            if cachecheck is not None and cachecheck != "fail":
                return cachecheck
    else:
        cachecheck = findPost("Playerdata", position, "name", playername)
        if cachecheck is not None and cachecheck != "fail":
            return cachecheck
    rosters = findManyPost("Teamdata", "Rosters", "", "")
    for team in rosters:
        for player in team["roster"]:
            if playername == player["name"]:
                data = cachePlayer(player["id"])
                return data
    return "No Player Found."

def playerFinderbyID(playerid,position = None):
    cachecheck = None
    if position is None:
        db = cluster["Playerdata"]
        positions = db.list_collection_names()
        for position in positions:
            cachecheck = findPost("Playerdata", position, "_id", playerid)
            if cachecheck is not None and cachecheck != "fail":
                return cachecheck
    else:
        cachecheck = findPost("Playerdata", position, "_id", playerid)
        if cachecheck is not None and cachecheck != "fail":
            return cachecheck
    data = cachePlayer(playerid)
    return data


def teamFinderbyName(teamname):
    return findPost("Teamdata", "Teams", "name", teamname)

def teamFinderbyID(teamid):
    return findPost("Teamdata", "Teams", "_id", teamid)


def getTeamRoster(teamname):
    data = findPost("Teamdata", "Rosters", "name", teamname)
    return data["roster"]


# noinspection PyTypeChecker
def getPlayerStats(playername,seasontype,year,position,output):

    data = playerFinderbyName(playername,position)

    for season in data["seasons"]:
        if season["type"] == seasontype and season["year"] == year:
            for team in season["teams"]:
                statistics = team["statistics"]
                if output:
                    print(playername + "'s " + str(year) + " " + seasontype + " statistics:")
                    if data["position"] == "QB":
                        passing = statistics["passing"]
                        print("\nPASSING:")
                        for stats in passing:
                            print(stats + " : " + str(passing[stats]))
                        if "rushing" in statistics:
                            print("\nRUSHING:")
                            rushing = statistics["rushing"]
                            for stats in rushing:
                                print(stats + " : " + str(rushing[stats]))
                        if "receiving" in statistics:
                            print("\nRECEIVING:")
                            receiving = statistics["receiving"]
                            for stats in receiving:
                                print(stats + " : " + str(receiving[stats]))
                    elif data["position"] == "RB":
                        print("\nRUSHING:")
                        rushing = statistics["rushing"]
                        for stats in rushing:
                            print(stats + " : " + str(rushing[stats]))
                        if "receiving" in statistics:
                            print("\nRECEIVING:")
                            receiving = statistics["receiving"]
                            for stats in rushing:
                                print(stats + " : " + str(receiving[stats]))
                        if "passing" in statistics:
                            print("\nPASSING:")
                            passing = statistics["passing"]
                            for stats in passing:
                                print(stats + " : " + str(passing[stats]))
                    elif data["position"] == "WR" or data["position"] == "TE":
                        print("\nRECEIVING:")
                        receiving = statistics["receiving"]
                        for stats in receiving:
                            print(stats + " : " + str(receiving[stats]))
                        if "rushing" in statistics:
                            print("\nRUSHING:")
                            rushing = statistics["rushing"]
                            for stats in rushing:
                                print(stats + " : " + str(rushing[stats]))
                        if "passing" in statistics:
                            print("\nPASSING:")
                            passing = statistics["passing"]
                            for stats in passing:
                                print(stats + " : " + str(passing[stats]))
                    elif data["position"] == "K":
                        print("KICKING")
                else:
                    return statistics
            break


# noinspection PyTypeChecker
def draftAnalyisis_RB(playername):
    data = playerFinderbyName(playername,"RB")
    if data["position"] != "RB":
        return "Not an RB"
    statistics = getPlayerStats(playername,"REG",2023,False)
    output_stats = {"name" : playername,
                    "RuAtt/game": round(statistics["rushing"]["attempts"] / statistics["games_played"],2),
                    "Tgts/game": round(statistics["receiving"]["targets"] / statistics["games_played"],2),
                    "YFS/game":round((statistics["rushing"]["yards"]+statistics["receiving"]["yards"])/statistics["games_played"],2),}
    output_stats["Touches/game"] = round(output_stats["RuAtt/game"] + statistics["receiving"]["receptions"] / statistics["games_played"],2)
    return output_stats
