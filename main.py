# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from SearchFunctions import *
from SearchFunctions import cachePlayer
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
from api_key import apikey
import requests
from databasefunctions import *
import requests
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = 1
    #getPlayerStats("Justin Tucker","REG",2023,True)
    #print(playerFinderbyName("Tyron Smith"))
    #print(draftAnalyisis_RB("Christian McCaffrey"))
    #print(draftAnalyisis_RB("Kyren Williams"))
    #print(playerFinderbyName("Christian McCaffrey","RB"))
    #getPlayerStats("Justin Herbert","REG",2023,"QB",True)
    print(draftAnalyisis_RB("Gus Edwards"))