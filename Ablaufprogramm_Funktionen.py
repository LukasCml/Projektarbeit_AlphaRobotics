"""
Funktion:     Funktionen für die Ablaufprogramme
Ersteller:    Lukas Camehl, Bernd Rensen, Jannik Birk
Datum:        01. Dezemeber 2021
Version:      Version 2.1
"""

import urx
import time
from socket import *

""" Verbindungen """
robot = urx.Robot("172.17.13.30")
portRobot = 29999
ipRobot = "172.17.13.30"
s = socket(AF_INET, SOCK_STREAM)
s.connect((ipRobot, portRobot))
portPLC = 502
ipPLC = "172.17.13.14"

""" Variablen für Start Sequenz (Dashboard-Befehle) """

sendPlay = """play""" + "\n"
sendStop = """stop""" + "\n"
sendPowerOn = """power on""" + "\n"
sendBrakeRelease = """brake release""" + "\n"
sendrobotmode = """robotmode""" + "\n"
sendisRunning = """running""" + "\n"
sendgetProgram = """get loaded program""" + "\n"
sendPowerOff = """power off""" + "\n"
sendPause = """pause""" + "\n"

def robotmode():
    s.send(sendrobotmode.encode())
    time.sleep(1)
    return_robotmode = (s.recv(1024))
    return_robotmode_str = str(return_robotmode)
    return_robotmode_str = return_robotmode_str.lstrip("'b\\'Connected: Universal Robots Dashboard Server\n")
    return_robotmode_str = return_robotmode_str.lstrip("'mode: ")
    return_robotmode_str = return_robotmode_str.rstrip("\n'")
    return_robotmode_str = return_robotmode_str[:-2]
    return return_robotmode_str

def running():
    s.send(sendisRunning.encode())
    time.sleep(1)
    return_running = (s.recv(1024))
    return_running_str = str(return_running)
    return_running_str = return_running_str.lstrip("'b\\'Connected: Universal Robots Dashboard Server\n")
    return_running_str = return_running_str.lstrip("'Program running: ")
    return_running_str = return_running_str.rstrip("\n\'")
    return_running_str = return_running_str[:-2]
    return return_running_str

def loadedprogram():
    s.send(sendgetProgram.encode())
    time.sleep(1)
    return_sendgetProgram = (s.recv(1024))
    return_sendgetProgram_str = str(return_sendgetProgram)
    return_sendgetProgram_str = return_sendgetProgram_str.lstrip("b'Loaded program: ")
    return_sendgetProgram_str = return_sendgetProgram_str.rstrip("\\n'")
    return return_sendgetProgram_str

def startSequenz(programmName):
    programmName = str(programmName)
    sendProgram = """load """+programmName+""".urp""" + "\n"
    while True:
        s.send(sendStop.encode())
        s.send(sendPowerOff.encode())
        robotmode()

        if robotmode() == "POWER_OFF":
            print("Roboter wurde gestoppt")
            print("Roboter Power Off erreicht")
            break

    while True:
        s.send(sendProgram.encode())
        loadedprogram()

        if loadedprogram() == "/programs/"+programmName+".urp":
            print("Programm wurde geladen")
            break

    while True:
        s.send(sendPowerOn.encode())
        robotmode()

        if robotmode() == "IDLE":
            print("Roboter Leerlauf erreicht")
            break

    while robotmode() == "IDLE":
        s.send(sendBrakeRelease.encode())
        robotmode()

        if robotmode() == "POWER_ON":
            print("Roboter Power On erreicht")
            break

    while running() == "false":
        s.send(sendPlay.encode())
        running()

        if running() == "true":
            print("Programm wurde gestartet")
            break

##################################### Funktionen für Ebenenerstellung ##################################################

def xEbene1(x_grenze, x_zurueck, y_min, y_max, z_min, z_max, programm_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[0] < x_grenze:                                   # Begrenzung X-Achse
        if act_pos[1] < y_min and act_pos[1] > y_max:           # Bereich Y-Achse
            if act_pos[2] < z_min and act_pos[2] > z_max:       # Bereich Z-Achse
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere X-Position """
                robot.movel([x_zurueck, rob_pos[1], rob_pos[2], rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                return print("X-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def xEbene2(x_grenze, x_zurueck, y_min, y_max, z_min, z_max, programm_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[0] > x_grenze:                                   # Begrenzung X-Achse
        if act_pos[1] < y_min and act_pos[1] > y_max:           # Bereich Y-Achse
            if act_pos[2] < z_min and act_pos[2] > z_max:       # Bereich Z-Achse
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere X-Position """
                robot.movel([x_zurueck, rob_pos[1], rob_pos[2], rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                return print("X-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def yEbene(y_grenze, y_zurueck, x_min, x_max, z_min, z_max, programm_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[1] > y_grenze:                                   # Begrenzung Y-Achse
        if act_pos[0] < x_min and act_pos[0] > x_max:           # Bereich X-Achse
            if act_pos[2] < z_min and act_pos[2] > z_max:       # Bereich Z-Achse
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere Y-Position """
                robot.movel([rob_pos[0], y_zurueck, rob_pos[2], rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                return print("Y-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def zEbene1(z_grenze, z_zurueck, x_min, x_max, y_min, y_max, programm_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[2] < z_grenze:                                   # Begrenzung Z-Achse
        if act_pos[0] < x_min and act_pos[0] > x_max:           # Bereich X-Achse
            if act_pos[1] < y_min and act_pos[1] > y_max:       # Bereich Y-Achse
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere Z-Position """
                robot.movel([rob_pos[0], rob_pos[1], z_zurueck, rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                return print("Z-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def zEbene2(z_grenze, z_zurueck, x_min, x_max, y_min, y_max, programm_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[2] > z_grenze:                                   # Begrenzung Z-Achse
        if act_pos[0] < x_min and act_pos[0] > x_max:           # Bereich X-Achse
            if act_pos[1] < y_min and act_pos[1] > y_max:       # Bereich Y-Achse
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere Z-Position """
                robot.movel([rob_pos[0], rob_pos[1], z_zurueck, rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                return print("Z-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def basisGelenkgrenze1(basis_grenze, basis_zurueck, programm_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] > basis_grenze:
        rob_joint_pos = robot.getj()
        """ Bewege den Robter in eine sichere Basis Position """
        robot.movej([basis_zurueck, rob_joint_pos[1], rob_joint_pos[2], rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
        s.send(sendPlay.encode())
        return print("Basis Gelenkgrenze "+programm_nr+" wurde angefahren")


def basisGelenkgrenze2(basis_grenze, basis_zurueck, programm_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] < basis_grenze:
        rob_joint_pos = robot.getj()
        """ Bewege den Robter in eine sichere Basis Position """
        robot.movej([basis_zurueck, rob_joint_pos[1], rob_joint_pos[2], rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
        s.send(sendPlay.encode())
        return print("Basis Gelenkgrenze "+programm_nr+" wurde angefahren")


def schulterGelenkgrenze1(schulter_grenze, schulter_zurueck, basis_min, basis_max, programm_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] > basis_min and act_joint_pos[0] < basis_max:
        if act_joint_pos[1] > schulter_grenze:
            rob_joint_pos = robot.getj()
            """ Bewege den Roboter in eine sichere Schulter Position """
            robot.movej([rob_joint_pos[0], schulter_zurueck, rob_joint_pos[2], rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
            s.send(sendPlay.encode())
            return print("Schulter Gelenkgrenze "+programm_nr+" wurde angefahren")


def schulterGelenkgrenze2(schulter_grenze, schulter_zurueck, ellbogen_zurueck, basis_min, basis_max, programm_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] > basis_min and act_joint_pos[0] < basis_max:
        if act_joint_pos[1] < schulter_grenze:
            rob_joint_pos = robot.getj()
            """ Bewege den Roboter in eine sichere Schulter Position """
            robot.movej([rob_joint_pos[0], schulter_zurueck, ellbogen_zurueck, rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
            s.send(sendPlay.encode())
            return print("Schulter Gelenkgrenze "+programm_nr+" wurde angefahren")


def ellbogenGelenkgrenze(ellbogen_grenze, ellbogen_zurueck, programm_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[2] < ellbogen_grenze:
        rob_joint_pos = robot.getj()
        """ Bewege den Roboter in eine sichere Ellbogen Position """
        robot.movej([rob_joint_pos[0], rob_joint_pos[1], ellbogen_zurueck, rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
        s.send(sendPlay.encode())
        return print("Ellbogen Gelenkgrenze "+programm_nr+" wurde angefahren")


def startStop():
    while True:
        eingabe = input("Um Kamerafahrt zu stoppen bzw. wieder zu starten, 'anhalten' oder 'weiter' eingeben!")
        if eingabe == 'anhalten':
            s.send(sendPause.encode())
        elif eingabe == 'weiter':
            s.send(sendPlay.encode())
        else:
            startStop()
