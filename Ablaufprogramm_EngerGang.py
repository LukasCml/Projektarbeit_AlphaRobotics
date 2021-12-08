"""
Funktion:     Ablaufprogramm Enger Gang
Ersteller:    Lukas Camehl, Bernd Rensen, Jannik Birk
Datum:        06. Dezemeber 2021
Version:      Version 2.2
"""

from Ablaufprogramme_Funktionen_CommunicationScript import *

""" Verbindung Dashboard Server"""
portRobot = 29999
ipRobot = "172.17.13.30"
s = socket(AF_INET, SOCK_STREAM)
s.connect((ipRobot, portRobot))
robot = urx.Robot("172.17.13.30")
sendPlay = """play""" + "\n"


def datenAuslesen():

    robotmode()
    running()
    loadedprogram()
    programstate()
    safetystatus()
    remoteControl()

def main():

    #start3DMouse('C:\Python_Programme\Roboter-Manipulatorarm-Ablaufprogramme\Maus-EngerGang', '3D_Mouse_Move.exe')
    startSequenz('engerGang')

    count = 0
    while count < 1:
        robot.movej([1.48, -0.698, 0.942, -3.089, -1.57, 3.14], acc=0.3, vel=1)
        count = count + 1
        s.send(sendPlay.encode())

    while True:
########################################## Erstellung der Ebenen #######################################################

        """ X-Ebenen """
        ### Ebene 1 ### (>)
        #xEbene2(-0.300, -0.299, 0.305, -0.890, 0.130, -0.58, '1', 32767)

        ### Ebene 2 ### (>)
        xEbene2(0.251, 0.250, 1.5, -1.5, 1.5, -0.58, '2', 16383)

        ### Ebene 3 ### (<)
        xEbene1(-0.320, -0.319, 1.5, -1.5, 1.5, -0.58, '3', 8191)

        """ Y-Ebenen """
        ### Ebene 1 ### (>)
        yEbene(-0.935, -0.936, 0, -0.228, 0.1, -0.58, '1', 4095)

        ### Ebene 2 ### (>)
        yEbene(0.1, 0.099, 1.5, -1.5, 1.5, -0.58, '2', 2047)

        """ Z-Ebene """
        ### Ebene 1 ### (<)
        zEbene1(0.327, 0.328, 0.240, -0.228, 0.110, -0.550, '1', 1023)

        ### Ebene 2 ### (<)
        zEbene1(0.237, 0.238, 0.240, -0.228, -0.550, -0.930, '2', 511)

        ### Ebene 3 ### (<)
        zEbene1(0.067, 0.068, 0.240, 0.025, -0.930, -1.125, '3', 255)

        ### Ebene 4 ### (<)
        zEbene1(-0.63, -0.62, 1.5, -1.5, 1.5, -1.5, '4', 127)

################################################### GELENKGRENZEN ######################################################

        """ Basis """
        ### Gelenkgrenze 1 ### (>)
        basisGelenkgrenze1(1.57, 1.525, '1', 32767)

        ### Gelenkgrenze 2 ### (<)
        basisGelenkgrenze2(1.3, 1.31, '2', 16383)

        """ Schulter """
        ### Schulter Gelenkgrenze 1 ### (>)
        schulterGelenkgrenze1(-0.395, -0.396, 0.785, 1.6, '1', 8191)

        ### Schulter Gelenkgrenze 2 ### (>)
        schulterGelenkgrenze1(0.1, 0.099, 0, 0.785, '2', 4095)

        ### Schulter Gelenkgrenze 3 ### (<)
        schulterGelenkgrenze2(-1.04, -1.03, 1.22, 1.3, 1.57, '3', 2047)

        """ Ellbogen """
        ### Ellbogen Gelenkgrenze 1 ### (<)
        ellbogenGelenkgrenze(0.4, 0.41, '1', 1023)


if __name__ == "__main__":
    try:
        datenAuslesen()
        main()

    except:
        s.send(sendStop.encode())
        print("Es ist ein Fehler aufgetreten")

