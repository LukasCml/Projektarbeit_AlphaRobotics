"""
Funktion:     Ablaufprogramm Grundstellungsfahrt
Ersteller:    Lukas Camehl, Bernd Rensen, Jannik Birk
Datum:        01. Dezemeber 2021
Version:      Version 1.5
"""

from Ablaufprogramme_Funktionen_CommunicationScript import *

""" Verbindung Robot Dashboard Server """
portRobot = 29999
ipRobot = "172.17.13.30"
s = socket(AF_INET, SOCK_STREAM)
s.connect((ipRobot, portRobot))

if __name__ == "__main__":

    grundstellung_erreicht = False
    sendStop = "stop" + "\n"
    robotmode()
    running()
    loadedprogram()
    programstate()
    safetystatus()
    remoteControl()
    startSequenz('homefahrt')

    try:
        while True:

############################################ Grundstellung schon erreicht ##############################################

            aktuelle_Position = robot.getl()
            if aktuelle_Position[0] > 0.170 and aktuelle_Position[0] < 0.180:
                if aktuelle_Position[1] > -0.275 and aktuelle_Position[1] < -0.265:             # 30.11 Korrekt !!!
                    if aktuelle_Position[2] > 0.515 and aktuelle_Position[2] < 0.525:
                        grundstellung_erreicht = True
                        print("Grundstellung schon erreicht")
                        robot.close()
                        break

############################################ Grundstellungsfahrt #######################################################
            time.sleep(2)
            aktuelle_Gelenk_Positionen = robot.getj()
            if grundstellung_erreicht == False:

                ######### Basis zwischen 25° und 90° ##########

                if aktuelle_Gelenk_Positionen[0] > 0.436 and aktuelle_Gelenk_Positionen[0] < 1.57:
                    if aktuelle_Gelenk_Positionen[2] < 1.57:
                        rob_position1 = robot.getj()
                        robot.movej([0, rob_position1[1], rob_position1[2], rob_position1[3], rob_position1[4], rob_position1[5]], acc=0.5, vel=1)
                        print("Position 1 erreicht")

                        rob_position2 = robot.getj()
                        robot.movej([rob_position2[0], -0.38, rob_position2[2], rob_position2[3], rob_position2[4], rob_position2[5]], acc=0.5, vel=1)
                        print("Position 2 erreicht")

                        rob_position3 = robot.getj()
                        robot.movej([rob_position3[0], rob_position3[1], 0, rob_position3[3], rob_position3[4], rob_position3[5]], acc=0.5, vel=1)
                        print("Position 3 erreicht")

                        rob_position4 = robot.getj()
                        robot.movej([rob_position4[0], rob_position4[1], rob_position4[2], rob_position4[3], -1.57, rob_position4[5]], acc=0.5, vel=1)
                        print("Position 4 erreicht")

                        rob_position5 = robot.getj()
                        robot.movej([rob_position5[0], rob_position5[1], rob_position5[2], 0, rob_position5[4], rob_position5[5]], acc=0.5, vel=1)
                        print("Position 5 erreicht")

                        rob_position6 = robot.getj()
                        robot.movej([rob_position6[0], rob_position6[1], rob_position6[2], rob_position6[3], rob_position6[4], 3.14], acc=0.5, vel=1)
                        print("Position 6 erreicht")

                        rob_position7 = robot.getj()
                        robot.movej([1.55, rob_position7[1], -2.79, rob_position7[3], rob_position7[4], rob_position7[5]], acc=0.5, vel=1)
                        print("Position 7 erreicht")

                        grundstellung_erreicht = True
                        print("Grundstellung erreicht")
                        s.send(sendStop.encode())
                        robot.close()
                        break

                if aktuelle_Gelenk_Positionen[0] > 0.436 and aktuelle_Gelenk_Positionen[0] < 1.57:
                    if aktuelle_Gelenk_Positionen[2] > 1.57:
                        rob_position1 = robot.getj()
                        robot.movej([rob_position1[0], rob_position1[1], 0, rob_position1[3], rob_position1[4], rob_position1[5]], acc=0.5, vel=1)
                        print("Position 1 erreicht")

                        rob_position2 = robot.getj()
                        robot.movej([rob_position2[0], -0.38, rob_position2[2], rob_position2[3], rob_position2[4], rob_position2[5]], acc=0.5, vel=1)
                        print("Position 2 erreicht")

                        rob_position3 = robot.getj()
                        robot.movej([0, rob_position3[1], rob_position3[2], rob_position3[3], rob_position3[4], rob_position3[5]], acc=0.5, vel=1)
                        print("Position 3 erreicht")

                        rob_position4 = robot.getj()
                        robot.movej([rob_position4[0], rob_position4[1], rob_position4[2], rob_position4[3], -1.57, rob_position4[5]], acc=0.5, vel=1)
                        print("Position 4 erreicht")

                        rob_position5 = robot.getj()
                        robot.movej([rob_position5[0], rob_position5[1], rob_position5[2], 0, rob_position5[4], rob_position5[5]], acc=0.5, vel=1)
                        print("Position 5 erreicht")

                        rob_position6 = robot.getj()
                        robot.movej([rob_position6[0], rob_position6[1], rob_position6[2], rob_position6[3], rob_position6[4], 3.14], acc=0.5, vel=1)
                        print("Position 6 erreicht")

                        rob_position7 = robot.getj()
                        robot.movej([1.55, rob_position7[1], -2.79, rob_position7[3], rob_position7[4], rob_position7[5]], acc=0.5, vel=1)
                        print("Position 7 erreicht")

                        grundstellung_erreicht = True
                        print("Grundstellung erreicht")
                        s.send(sendStop.encode())
                        robot.close()
                        break

                ######### Basis zwischen 25° und -90° ##########

                if aktuelle_Gelenk_Positionen[0] > -1.57 and aktuelle_Gelenk_Positionen[0] < 0.436:
                    rob_position1 = robot.getj()
                    robot.movej([rob_position1[0], rob_position1[1], 0, rob_position1[3], rob_position1[4], rob_position1[5]], acc=0.5, vel=1)
                    print("Position 1 erreicht")

                    rob_position2 = robot.getj()
                    robot.movej([rob_position2[0], -0.38, rob_position2[2], rob_position2[3], rob_position2[4], rob_position2[5]], acc=0.5, vel=1)
                    print("Position 2 erreicht")

                    rob_position3 = robot.getj()
                    robot.movej([0, rob_position3[1], rob_position3[2], rob_position3[3], rob_position3[4], rob_position3[5]], acc=0.5, vel=1)
                    print("Position 3 erreicht")

                    rob_position4 = robot.getj()
                    robot.movej([rob_position4[0], rob_position4[1], rob_position4[2], rob_position4[3], -1.57, rob_position4[5]], acc=0.5, vel=1)
                    print("Position 4 erreicht")

                    rob_position5 = robot.getj()
                    robot.movej([rob_position5[0], rob_position5[1], rob_position5[2], 0, rob_position5[4], rob_position5[5]], acc=0.5, vel=1)
                    print("Position 5 erreicht")

                    rob_position6 = robot.getj()
                    robot.movej([rob_position6[0], rob_position6[1], rob_position6[2], rob_position6[3], rob_position6[4], 3.14], acc=0.5, vel=1)
                    print("Position 6 erreicht")

                    rob_position7 = robot.getj()
                    robot.movej([1.55, rob_position7[1], -2.79, rob_position7[3], rob_position7[4], rob_position7[5]], acc=0.5, vel=1)
                    print("Position 7 erreicht")

                    grundstellung_erreicht = True
                    print("Grundstellung erreicht")
                    s.send(sendStop.encode())
                    robot.close()
                    break

    except:
        print("Es ist ein Fehler aufgetreten")
        s.send(sendStop.encode())

    finally:
        robot.close()
