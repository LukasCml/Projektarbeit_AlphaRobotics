"""
Funktion:     Ablaufprogramm Showfahrt
Ersteller:    Lukas Camehl, Bernd Rensen, Jannik Birk
Datum:        02. Dezember 2021
Version:      Version 1.1
"""

from Ablaufprogramme_Funktionen_CommunicationScript import *

""" Verbindung Dashboard Server"""
portRobot = 29999
ipRobot = "172.17.13.30"
s = socket(AF_INET, SOCK_STREAM)
s.connect((ipRobot, portRobot))
robot = urx.Robot("172.17.13.30")
sendPlay = "play" + "\n"

def datenAuslesen():

    robotmode()
    running()
    loadedprogram()
    programstate()
    safetystatus()
    remoteControl()

def main():

    startSequenz('showfahrt')

if __name__ == "__main__":
    try:
        datenAuslesen()
        main()

    except:
        s.send(sendStop.encode())
        print("Es ist ein Fehler aufgetreten")


