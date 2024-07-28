import requests
import time
from api_key import apikey
from databasefunctions import *
import csv



def cachePlayer(id):
    time.sleep(2)
    url = "https://api.sportradar.com/nfl/official/trial/v7/en/players/" + id + "/profile.json?api_key=" + apikey

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        data["_id"] = data.pop("id")
        addPost("Playerdata", data["position"], data)
        return data
    except:
        return cachePlayer(id)


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

    statistics = getPlayerStats(playername,"REG",2022,"RB",False)
    if statistics == "No Player Found.":
        return statistics
    output_stats = {"name" : playername,
                    "RuAtt/game": round(statistics["rushing"]["attempts"] / statistics["games_played"],2),
                    "Tgts/game": round(statistics["receiving"]["targets"] / statistics["games_played"],2),
                    "YFS/game":round((statistics["rushing"]["yards"]+statistics["receiving"]["yards"])/statistics["games_played"],2),}
    output_stats["Touches/game"] = round(output_stats["RuAtt/game"] + statistics["receiving"]["receptions"] / statistics["games_played"],2)
    return output_stats

def draftAnalyisis_QB(playername):
    statistics = getPlayerStats(playername,"REG",2022,"QB",False)
    if statistics == "No Player Found.":
        return statistics
    output_stats = {"name" : playername}
    if "rushing" in statistics:
        output_stats["RuYd/Game"] = statistics["rushing"]["yards"]/statistics["games_played"]
    if "passing" in statistics:
        output_stats["Comp%"] = statistics["passing"]["completions"]/statistics["passing"]["attempts"]
    return output_stats


def getAllPositionStats(position):
    rosters = findManyPost("Teamdata", "Rosters", "", "")
    for team in rosters:
        for player in team["roster"]:
            if player["position"] == position:
                cachecheck = findPost("Playerdata",position,"_id",player["id"])
                if cachecheck is None:
                    data = cachePlayer(player["id"])

def RB_outputToCSV():
    players = findManyPost("Playerdata","RB","","")
    data = []
    for player in players:
        output_stats = {}
        for season in player["seasons"]:
            if season["type"] == "REG" and season["year"] == 2022:
                rushatt = 0
                touches = 0
                targets = 0
                receptions = 0
                yardsfromscrimmage = 0
                gamesplayed = 0
                for team in season["teams"]:
                    statistics = team["statistics"]
                    if ("receiving" in statistics) and ("rushing" in statistics):
                        targets += statistics["receiving"]["targets"]
                        receptions += statistics["receiving"]["receptions"]
                        rushatt += statistics["rushing"]["attempts"]
                        touches += statistics["rushing"]["attempts"] + statistics["receiving"]["receptions"]
                        yardsfromscrimmage += statistics["rushing"]["yards"]+statistics["receiving"]["yards"]
                    elif "rushing" in statistics:
                        yardsfromscrimmage += statistics["rushing"]["yards"]
                        rushatt += statistics["rushing"]["attempts"]
                        touches += statistics["rushing"]["attempts"]
                    elif "receiving" in statistics:
                        yardsfromscrimmage += statistics["receiving"]["yards"]
                        touches += statistics["receiving"]["receptions"]
                        targets += statistics["receiving"]["targets"]
                        receptions += statistics["receiving"]["receptions"]
                    gamesplayed += statistics["games_played"]

                if gamesplayed > 4:
                    output_stats["name"] = player["name"]
                    output_stats["Rush_Att/Game"] = rushatt/gamesplayed
                    output_stats["Targets/Game"] = targets/gamesplayed
                    output_stats["YFS/Game"] = yardsfromscrimmage/gamesplayed
                    output_stats["Touches/Game"] = touches/gamesplayed
                    output_stats["Receptions/Game"] = receptions/gamesplayed
                else:
                    break

            elif season["type"] == "REG" and season["year"] == 2023:
                points = 0
                gamesplayed = 0
                for team in season["teams"]:
                    statistics = team["statistics"]
                    gamesplayed += statistics["games_played"]
                    if "receiving" in statistics:
                        points += statistics["receiving"]["receptions"]
                        points += statistics["receiving"]["yards"]*0.1
                        points += statistics["receiving"]["touchdowns"]*6
                    if "fumble" in statistics:
                        points -= statistics["fumbles"]["lost_fumbles"]*2
                    if "rushing" in statistics:
                        points += statistics["rushing"]["yards"]*0.1
                        points += statistics["rushing"]["touchdowns"]*6
                output_stats["fantasy_points_2023"] = points
                if gamesplayed < 4 or points == 0:
                    if "name" in output_stats:
                        output_stats.pop("name")
        if "name" in output_stats:
            data.append(output_stats)

    data.sort(key=lambda x: x["fantasy_points_2023"],reverse=True)
    count = 1
    for player in data:
        player["fantasy_finish"] = count
        count += 1




    with open("RB_Stats.csv","w",newline="") as f:
        fieldnames = ["name","Rush_Att/Game","Targets/Game","YFS/Game","Touches/Game","Receptions/Game","fantasy_points_2023","fantasy_finish"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def RB_2024Predictor():
    players = findManyPost("Playerdata", "RB", "", "")
    data = []
    for player in players:
        output_stats = {}
        for season in player["seasons"]:
            if season["type"] == "REG" and season["year"] == 2023:
                rushatt = 0
                touches = 0
                targets = 0
                receptions = 0
                yardsfromscrimmage = 0
                gamesplayed = 0
                for team in season["teams"]:
                    statistics = team["statistics"]
                    if ("receiving" in statistics) and ("rushing" in statistics):
                        targets += statistics["receiving"]["targets"]
                        receptions += statistics["receiving"]["receptions"]
                        rushatt += statistics["rushing"]["attempts"]
                        touches += statistics["rushing"]["attempts"] + statistics["receiving"]["receptions"]
                        yardsfromscrimmage += statistics["rushing"]["yards"] + statistics["receiving"]["yards"]
                    elif "rushing" in statistics:
                        yardsfromscrimmage += statistics["rushing"]["yards"]
                        rushatt += statistics["rushing"]["attempts"]
                        touches += statistics["rushing"]["attempts"]
                    elif "receiving" in statistics:
                        yardsfromscrimmage += statistics["receiving"]["yards"]
                        touches += statistics["receiving"]["receptions"]
                        targets += statistics["receiving"]["targets"]
                        receptions += statistics["receiving"]["receptions"]
                    gamesplayed += statistics["games_played"]

                if gamesplayed > 4:
                    output_stats["name"] = player["name"]
                    output_stats["YFS/Game"] = yardsfromscrimmage / gamesplayed
                    output_stats["Touches/Game"] = touches / gamesplayed

                    pred_finish = 59.41 - 0.698*output_stats["YFS/Game"] + 1.23*output_stats["Touches/Game"]
                    pred_points = 33.5 + 3.41*output_stats["YFS/Game"] -7.8*output_stats["Touches/Game"]
                    output_stats["fantasy_finish"] = round(pred_finish,2)
                    output_stats["predicted_points"] = round(pred_points,2)

                    data.append(output_stats)
    data.sort(key=lambda x: x["fantasy_finish"],reverse=False)
    return data



def QB_outputToCSV():
    players = findManyPost("Playerdata", "QB", "", "")
    data = []
    for player in players:
        output_stats = {}
        for season in player["seasons"]:
            if season["type"] == "REG" and season["year"] == 2022:
                games_played = 0
                rush_yards = 0
                attempts = 0
                completions = 0
                for team in season["teams"]:
                    statistics = team["statistics"]
                    games_played += statistics["games_played"]
                    if "rushing" in statistics:
                        rush_yards += statistics["rushing"]["yards"]
                    if "passing" in statistics:
                        attempts += statistics["passing"]["attempts"]
                        completions += statistics["passing"]["completions"]
                if games_played > 8 and attempts > 100:
                    output_stats["name"] = player["name"]
                    output_stats["RuYd/Game"] = rush_yards/games_played
                    output_stats["Comp%"] = completions/attempts
                else:
                    break
            elif season["type"] == "REG" and season["year"] == 2023:
                points = 0
                games_played = 0
                for team in season["teams"]:
                    statistics = team["statistics"]
                    games_played += statistics["games_played"]
                    if "rushing" in statistics:
                        points += statistics["rushing"]["yards"]*0.1
                        points += statistics["rushing"]["touchdowns"]*6
                    if "passing" in statistics:
                        points += statistics["passing"]["yards"]*.04
                        points += statistics["passing"]["touchdowns"]*4
                        points -= statistics["passing"]["interceptions"]*2
                    if "fumble" in statistics:
                        points -= statistics["fumbles"]["lost_fumbles"]*2
                if games_played > 8 and points > 50:
                    output_stats["fantasy_points_2023"] = points
        if "name" in output_stats and "fantasy_points_2023" in output_stats:
            data.append(output_stats)
    data.sort(key=lambda x: x["fantasy_points_2023"],reverse=True)
    count = 1
    for player in data:
        player["fantasy_finish"] = count
        count += 1

    with open("QB_Stats.csv","w",newline="") as f:
        fieldnames = ["name","RuYd/Game","Comp%","fantasy_points_2023","fantasy_finish"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)



def QB_2024Predictor():
    players = findManyPost("Playerdata", "QB", "", "")
    data = []
    for player in players:
        output_stats = {}
        for season in player["seasons"]:
            if season["type"] == "REG" and season["year"] == 2022:
                games_played = 0
                rush_yards = 0
                attempts = 0
                completions = 0
                for team in season["teams"]:
                    statistics = team["statistics"]
                    games_played += statistics["games_played"]
                    if "rushing" in statistics:
                        rush_yards += statistics["rushing"]["yards"]
                    if "passing" in statistics:
                        attempts += statistics["passing"]["attempts"]
                        completions += statistics["passing"]["completions"]
                if games_played > 8 and attempts > 100:
                    output_stats["name"] = player["name"]
                    output_stats["RuYd/Game"] = rush_yards / games_played
                    output_stats["Comp%"] = completions / attempts
                else:
                    break

                if games_played > 8 and attempts > 100:
                    output_stats["name"] = player["name"]
                    output_stats["RuYd/Game"] = rush_yards / games_played
                    output_stats["Comp%"] = completions / attempts

                    pred_finish = 30.8 - 0.0874*output_stats["RuYd/Game"] - 28.7*output_stats["Comp%"]
                    #pred_points = 33.5 + 3.41*output_stats["Comp%"]



