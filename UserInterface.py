import SearchFunctions


class UserInterface:
    def __init__(self):
        self.SearchFunctions = SearchFunctions.SearchFunctions()

    def userPlayerFinder(self):
        player = input("Please enter player name you wish to view:")

        data = self.SearchFunctions.playerFinder(player)
        if(data == "Retrival Error" or data == "No Player Found."):
            print(data)
            return 0
        for item in data:
            if (item == "_comment") or (item == "seasons"):
                continue
            print("item: " + item)
            print("value: " + str(data[item]))
            print("-------------------------")
        fetch = input("Please input season you wish to view.")
        for season in data['seasons']:
            if str(season['year']) == str(fetch):
                for team in season['teams']:
                    for stat in team["statistics"]: # NEED TO KEEP INTERATING THROUGH STAT DICTIONARIES SO EACH STAT PRINTS ON NEW LINE
                        print(stat + ": " + str(team["statistics"][stat]))
                    #print(item + ": " + str(season['teams']['statistics'][item]))





        #print(data["seasons"][1]["statistics"])
        #for items in data:
         #   print(items +": "+ str(data[items]))
        #for items in data["seasons"]:
           # print(items)
    def userTeamFinder(self):
        team = input("Please enter team name you wish to view:")

        data = self.SearchFunctions.teamFinder(team)
        if data == "Retrival Error" or data == "No Team Found.":
            print(data)
            return 0
        print("Name: " + data["name"])
        print(data)
