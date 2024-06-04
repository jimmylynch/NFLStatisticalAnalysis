# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import time
    import requests
    import json
    import UserInterface
    import requests
    import morsecodesolver
    #vals = ".--.-...---...-...---..-."
    vals = ".-..---...-...---...-.--."
    morsecodesolver.morsecode("",vals)
    newvals = ""
    for n in range(0,len(vals)-1):
        if vals[n] == ".":
            newvals += "-"
        else:
            newvals += "."
    #morsecodesolver.morsecode("",newvals)
   # newrun = UserInterface.UserInterface()
    #while 1:
     #   newrun.userPlayerFinder()
