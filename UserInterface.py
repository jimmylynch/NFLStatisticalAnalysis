import SearchFunctions


class UserInterface:
    def __init__(self):
        self.SearchFunctions = SearchFunctions.SearchFunctions()

    def userPlayerFinder(self, name="name", id="id"):
        player = input("Please enter player name you wish to view:")

        data = self.SearchFunctions.playerFinder(player)
        if(data == "Retrival Error"):
            print(data)
            return 0
        print(data)
        print("Name: " + data["name"])

