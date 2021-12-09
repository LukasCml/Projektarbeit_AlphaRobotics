"""
Alpha WOLF

Company:            Alpha Robotics Germany GmbH & Co. KG
                    Alter Flugplatz 38
                    49377 Vechta
                    Germany
Author:             D. Rieken, J. Strauch, L. Camehl
Last Modification:  06.12.2021
Version:            1.2
Copy Rights:        Alpha Robotics Germany GmbH & Co. KG
"""

import urx
import os
import time
from socket import *
import sys
from pyModbusTCP.client import ModbusClient


""" Verbindungen """

robot = urx.Robot("172.17.13.30")
portRobot = 29999
ipRobot = "172.17.13.30"
s = socket(AF_INET, SOCK_STREAM)
s.connect((ipRobot, portRobot))
portPLC = 502
ipPLC = "172.17.13.14"

""" Dashboard-Befehle """
extension = "\n"
sendPlay = "play" + extension
sendStop = "stop" + extension
sendPowerOn = "power on" + extension
sendBrakeRelease = "brake release" + extension
sendrobotmode = "robotmode" + extension
sendisRunning = "running" + extension
sendgetProgram = "get loaded program" + extension
sendPowerOff = "power off" + extension
sendPause = "pause" + extension
sendProgramState = "programstate" + extension
sendSafetyStatus = "safetystatus" + extension
sendRemoteControl = "is in remote control" + extension

####################################################### ROBOTMODE ######################################################

def robotmode():
    s.send(sendrobotmode.encode())
    time.sleep(1)
    return_robotmode = (s.recv(1024))
    return_robotmode_str = str(return_robotmode)
    return_robotmode_str = return_robotmode_str.lstrip("'b\\'Connected: Universal Robots Dashboard Server\n")
    return_robotmode_str = return_robotmode_str.lstrip("'mode: ")
    return_robotmode_str = return_robotmode_str.rstrip("\n'")
    return_robotmode_str = return_robotmode_str[:-2]

    if return_robotmode_str == "RUNNING":
        writeRegister(2, 32767)
        return "NORMAL"
    elif return_robotmode_str == "NO_CONTROLLER":
        writeRegister(2, 16383)
        return "NO_CONTROLLER"
    elif return_robotmode_str == "DISCONNECTED":
        writeRegister(2, 8191)
        return "DISCONNECTED"
    elif return_robotmode_str == "CONFIRM_SAFETY":
        writeRegister(2, 4095)
        return "CONFIRM_SAFETY"
    elif return_robotmode_str == "BOOTING":
        writeRegister(2, 2047)
        return "BOOTING"
    elif return_robotmode_str == "POWER_OFF":
        writeRegister(2, 1023)
        return "POWER_OFF"
    elif return_robotmode_str == "POWER_ON":
        writeRegister(2, 511)
        return "POWER_ON"
    elif return_robotmode_str == "IDLE":
        writeRegister(2, 255)
        return "IDLE"
    elif return_robotmode_str == "BACKDRIVE":
        writeRegister(2, 127)
        return "BACKDRIVE"

############################################### ROBOTMODE ENDE #########################################################

################################################## RUNNING #############################################################

def running():
    s.send(sendisRunning.encode())
    time.sleep(1)
    return_running = (s.recv(1024))
    return_running_str = str(return_running)
    return_running_str = return_running_str.lstrip("'b\\'Connected: Universal Robots Dashboard Server\n")
    return_running_str = return_running_str.lstrip("'Program running: ")
    return_running_str = return_running_str.rstrip("\n\'")
    return_running_str = return_running_str[:-2]

    if return_running_str == "true":
        writeRegister(4, 32767)
        return "TRUE"
    elif return_running_str == "false":
        writeRegister(4, 1)
        return "FALSE"

############################################### RUNNING ENDE ###########################################################

############################################## LOADED PROGRAM ##########################################################

def loadedprogram():
    s.send(sendgetProgram.encode())
    time.sleep(1)
    return_sendgetProgram = (s.recv(1024))
    return_sendgetProgram_str = str(return_sendgetProgram)
    return_sendgetProgram_str = return_sendgetProgram_str.lstrip("b'Loaded program: ")
    return_sendgetProgram_str = return_sendgetProgram_str.rstrip("\\n'")

    if return_sendgetProgram_str == "/programs/3dmouse_move_normal.urp":
        writeRegister(18, 6)
        return "3dmouse_move_normal"
    elif return_sendgetProgram_str == "/programs/engerGang.urp":
        writeRegister(18, 5)
        return "engerGang"
    elif return_sendgetProgram_str == "/programs/geringeDeckenhoehe.urp":
        writeRegister(18, 4)
        return "geringeDeckenhoehe"
    elif return_sendgetProgram_str == "/programs/geringeDeckenhoeheStart.urp":
        writeRegister(18, 3)
        return "geringeDeckenhoeheStart"
    elif return_sendgetProgram_str == "/programs/visuelleLagesondierung.urp":
        writeRegister(18, 2)
        return "visuelleLagesondierung"
    elif return_sendgetProgram_str == "/programs/showfahrt.urp":
        writeRegister(18, 1)
        return "showfahrt"
    elif return_sendgetProgram_str == "/programs/homefahrt.urp":
        writeRegister(18, 0)
        return "homefahrt"

############################################# LOADED PROGRAM ENDE ######################################################

################################################# PROGRAMSTATE #########################################################

def programstate():
    s.send(sendProgramState.encode())
    time.sleep(1)
    return_programState = (s.recv(1024))
    return_programState_str = str(return_programState)
    return_programState_str = return_programState_str.lstrip("b'")
    return_programState_str = return_programState_str.rstrip(" engerGang.urp\\n'")

    if return_programState_str == "PLAYING":
        writeRegister(11, 100)
        return "PLAYING"
    elif return_programState_str == "PAUSED":
        writeRegister(11, 50)
        return "PAUSED"
    elif return_programState_str == "STOPPED":
        writeRegister(11, 1)
        return "STOPPED"

############################################### PROGRAM STATE ENDE #####################################################

################################################## SAFETYSTATUS ########################################################

def safetystatus():
    s.send(sendSafetyStatus.encode())
    time.sleep(1)
    return_safetyStatus = (s.recv(1024))
    return_safetyStatus_str = str(return_safetyStatus)
    return_safetyStatus_str = return_safetyStatus_str.lstrip("b'Safetystatus: ")
    return_safetyStatus_str = return_safetyStatus_str.rstrip("\\n'")

    if return_safetyStatus_str == "NORMAL":
        writeRegister(1, 32767)
        return "NORMAL"
    elif return_safetyStatus_str == "REDUCED":
        writeRegister(1, 16383)
        return "REDUCED"
    elif return_safetyStatus_str == "PROTECTIVE_STOP":
        writeRegister(1, 8191)
        return "PROTECTIVE_STOP"
    elif return_safetyStatus_str == "RECOVERY":
        writeRegister(1, 4095)
        return "RECOVERY"
    elif return_safetyStatus_str == "SAFEGUARD_STOP":
        writeRegister(1, 2047)
        return "SAFEGUARD_STOP"
    elif return_safetyStatus_str == "SYSTEM_EMERGENCY_STOP":
        writeRegister(1, 1023)
        return "SYSTEM_EMERGENCY_STOP"
    elif return_safetyStatus_str == "ROBOT_EMERGENCY_STOP":
        writeRegister(1, 511)
        return "ROBOT_EMERGENCY_STOP"
    elif return_safetyStatus_str == "VIOLATION":
        writeRegister(1, 255)
        return "VIOLATION"
    elif return_safetyStatus_str == "FAULT":
        writeRegister(1, 127)
        return "FAULT"
    elif return_safetyStatus_str == "AUTOMATIC_MODE_SAFEGUARD_STOP":
        writeRegister(1, 63)
        return "AUTOMATIC_MODE_SAFGUARD_STOP"
    elif return_safetyStatus_str == "SYSTEM_THREE_POSITION_ENABLING_STOP":
        writeRegister(1, 31)
        return "SYSTEM_THREE_POSITION_ENABLNG_STOP"

############################################## SAFETYSTATE ENDE ########################################################

############################################### REMOTE CONTROL #########################################################

def remoteControl():
    s.send(sendRemoteControl.encode())
    time.sleep(1)
    return_remoteControl = (s.recv(1024))
    return_remoteControl_str = str(return_remoteControl)
    return_remoteControl_str = return_remoteControl_str.lstrip("b'")
    return_remoteControl_str = return_remoteControl_str.rstrip("\\n'")
    time.sleep(1)

    if return_remoteControl_str == "true":
        writeRegister(8, 32767)
        return "TRUE"

    elif return_remoteControl_str == "false":
        writeRegister(8, 1)
        return "FALSE"

############################################# REMOTE CONROL ENDE #######################################################

################################################ START SEQUENZ #########################################################

def startSequenz(programmName):
    programmName = str(programmName)
    sendProgram = "load "+programmName+".urp" + "\n"
    while True:
        s.send(sendStop.encode())
        s.send(sendPowerOff.encode())
        robotmode()

        if robotmode() == "POWER_OFF":
            print("Roboter wurde gestoppt!")
            print("Roboter befindet sich in der Betriebsart: POWER OFF")
            break

    while True:
        s.send(sendProgram.encode())
        loadedprogram()

        if loadedprogram() == programmName:
            print(f"Programm '{loadedprogram()}' wurde geladen!")
            break

    while True:
        s.send(sendPowerOn.encode())
        robotmode()

        if robotmode() == "IDLE":
            print("Roboter befindet sich in der Betriebsart: IDLE!")
            break

    while robotmode() == "IDLE":
        s.send(sendBrakeRelease.encode())
        robotmode()

        if robotmode() == "NORMAL":
            print("Roboter befindet sich in der Betriebsart: NORMAL!")
            break

    while running() == "FALSE":
        s.send(sendPlay.encode())
        running()

        if running() == "TRUE":
            print(f"Programm '{loadedprogram()}' wurde gestartet!")
            break

########################################## START SEQUENZ ENDE ##########################################################

##################################### FUNKTIONEN FÜR EBENENERSTELLUNG ##################################################

def xEbene1(x_grenze, x_zurueck, y_min, y_max, z_min, z_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[0] < x_grenze:                                   # Begrenzung X-Achse
        if act_pos[1] < y_min and act_pos[1] > y_max:           # Bereich Y-Achse
            if act_pos[2] < z_min and act_pos[2] > z_max:       # Bereich Z-Achse
                writeRegister(20, register_nr)
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere X-Position """
                robot.movel([x_zurueck, rob_pos[1], rob_pos[2], rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                writeRegister(20, 0)
                return print("X-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def xEbene2(x_grenze, x_zurueck, y_min, y_max, z_min, z_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[0] > x_grenze:                                   # Begrenzung X-Achse
        if act_pos[1] < y_min and act_pos[1] > y_max:           # Bereich Y-Achse
            if act_pos[2] < z_min and act_pos[2] > z_max:       # Bereich Z-Achse
                writeRegister(20, register_nr)
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere X-Position """
                robot.movel([x_zurueck, rob_pos[1], rob_pos[2], rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                writeRegister(20, 0)
                return print("X-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def yEbene(y_grenze, y_zurueck, x_min, x_max, z_min, z_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[1] > y_grenze:                                   # Begrenzung Y-Achse
        if act_pos[0] < x_min and act_pos[0] > x_max:           # Bereich X-Achse
            if act_pos[2] < z_min and act_pos[2] > z_max:       # Bereich Z-Achse
                writeRegister(20, register_nr)
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere Y-Position """
                robot.movel([rob_pos[0], y_zurueck, rob_pos[2], rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                writeRegister(20, 0)
                return print("Y-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def zEbene1(z_grenze, z_zurueck, x_min, x_max, y_min, y_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[2] < z_grenze:                                   # Begrenzung Z-Achse
        if act_pos[0] < x_min and act_pos[0] > x_max:           # Bereich X-Achse
            if act_pos[1] < y_min and act_pos[1] > y_max:       # Bereich Y-Achse
                writeRegister(20, register_nr)
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere Z-Position """
                robot.movel([rob_pos[0], rob_pos[1], z_zurueck, rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                writeRegister(20, 0)
                return print("Z-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def zEbene2(z_grenze, z_zurueck, x_min, x_max, y_min, y_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_pos = robot.get_pos()
    if act_pos[2] > z_grenze:                                   # Begrenzung Z-Achse
        if act_pos[0] < x_min and act_pos[0] > x_max:           # Bereich X-Achse
            if act_pos[1] < y_min and act_pos[1] > y_max:       # Bereich Y-Achse
                writeRegister(20, register_nr)
                rob_pos = robot.getl()
                """ Bewege den Roboter in eine sichere Z-Position """
                robot.movel([rob_pos[0], rob_pos[1], z_zurueck, rob_pos[3], rob_pos[4], rob_pos[5]], acc=0.3, vel=0.5)
                s.send(sendPlay.encode())
                writeRegister(20, 0)
                return print("Z-Achse Sicherheitsebene "+programm_nr+" wurde angefahren")


def basisGelenkgrenze1(basis_grenze, basis_zurueck, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] > basis_grenze:
        writeRegister(22, register_nr)
        rob_joint_pos = robot.getj()
        """ Bewege den Robter in eine sichere Basis Position """
        robot.movej([basis_zurueck, rob_joint_pos[1], rob_joint_pos[2], rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
        s.send(sendPlay.encode())
        writeRegister(20, 0)
        return print("Basis Gelenkgrenze "+programm_nr+" wurde angefahren")


def basisGelenkgrenze2(basis_grenze, basis_zurueck, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] < basis_grenze:
        writeRegister(22, register_nr)
        rob_joint_pos = robot.getj()
        """ Bewege den Robter in eine sichere Basis Position """
        robot.movej([basis_zurueck, rob_joint_pos[1], rob_joint_pos[2], rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
        s.send(sendPlay.encode())
        writeRegister(20, 0)
        return print("Basis Gelenkgrenze "+programm_nr+" wurde angefahren")


def schulterGelenkgrenze1(schulter_grenze, schulter_zurueck, basis_min, basis_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] > basis_min and act_joint_pos[0] < basis_max:
        if act_joint_pos[1] > schulter_grenze:
            writeRegister(22, register_nr)
            rob_joint_pos = robot.getj()
            """ Bewege den Roboter in eine sichere Schulter Position """
            robot.movej([rob_joint_pos[0], schulter_zurueck, rob_joint_pos[2], rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
            s.send(sendPlay.encode())
            writeRegister(20, 0)
            return print("Schulter Gelenkgrenze "+programm_nr+" wurde angefahren")

############################################### EBENENERSTELLUNG ENDE ##################################################

################################################### GELENKGRENZEN ######################################################

def schulterGelenkgrenze2(schulter_grenze, schulter_zurueck, ellbogen_zurueck, basis_min, basis_max, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[0] > basis_min and act_joint_pos[0] < basis_max:
        if act_joint_pos[1] < schulter_grenze:
            writeRegister(22, register_nr)
            rob_joint_pos = robot.getj()
            """ Bewege den Roboter in eine sichere Schulter Position """
            robot.movej([rob_joint_pos[0], schulter_zurueck, ellbogen_zurueck, rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
            s.send(sendPlay.encode())
            writeRegister(20, 0)
            return print("Schulter Gelenkgrenze "+programm_nr+" wurde angefahren")


def ellbogenGelenkgrenze(ellbogen_grenze, ellbogen_zurueck, programm_nr, register_nr):
    programm_nr = str(programm_nr)
    act_joint_pos = robot.getj()
    if act_joint_pos[2] < ellbogen_grenze:
        writeRegister(22, register_nr)
        rob_joint_pos = robot.getj()
        """ Bewege den Roboter in eine sichere Ellbogen Position """
        robot.movej([rob_joint_pos[0], rob_joint_pos[1], ellbogen_zurueck, rob_joint_pos[3], rob_joint_pos[4], rob_joint_pos[5]], acc=0.3, vel=0.5)
        s.send(sendPlay.encode())
        writeRegister(20, 0)
        return print("Ellbogen Gelenkgrenze "+programm_nr+" wurde angefahren")

########################################### GELENKGRENZEN ENDE #########################################################

################################### START/STOP FÜR VISUELLE LAGESONDIERUNG #############################################

def startStop():
    while True:
        if readRegister(10, 1)[0] == 5:
            s.send(sendPause.encode())
        elif readRegister(10, 1)[0] == 10:
            s.send(sendPlay.encode())
        else:
            startStop()

################################## START/STOP FÜR VISUELLE LAGESONDIERUNG ENDE #########################################

###################################### FUNKTIONEN REGISTEREINTRÄGE #####################################################

def writeRegister(address, value):
    if plc.is_open:
        plc.write_single_register(address, value)
    else:
        writeRegister(13, 1)
        sys.exit()

def readRegister(address, number):
    if plc.is_open:
        return plc.read_holding_registers(address, number)
    else:
        writeRegister(13, 1)
        sys.exit()

###################################### FUNKTIONEN REGISTEREINTRÄGE ENDE ################################################

################################################### 3D MAUS ############################################################

def start3DMouse(path, programm):
    try:
        os.chdir(path)
        os.system(programm)
        return "3D Maus wurde gestartet"
    except:
        etype, evalue, etb = sys.exc_info()
        antwort = "Datei konnte nicht geöffnet werden\n" + "Fehler: " + str(evalue)
        return antwort

############################################## 3D MAUS ENDE ############################################################

############################################ MODBUS VERBINDUNG #########################################################

"""
Modbus connection to Schneider PLC
Schneider only supports
0x01 --> (Schneider: read digital outputs)          | (PyModbusTCP: read_coils(bit_addr, bit_nb=1))
0x02 --> (Schneider: read digital inputs)           | (PyModbusTCP: read_discrete_inputs(bit_addr, bit_nb=1))
0x03 --> (Schneider: read holding register)         | (PyModbusTCP: read_holding_registers(reg_addr, reg_nb=1))
0x06 --> (Schneider: write single register)         | (PyModbusTCP: write_single_register(reg_addr, reg_value))
0x08 --> (Schneider: diagnosis)                     | (PyModbusTCP: ---)
0x0F --> (Schneider: write multiple outputs)        | (PyModbusTCP: write_multiple_coils(bits_addr, bits_value))
0x10 --> (Schneider: write multiple registers)      | (PyModbusTCP: write_multiple_registers(regs_addr, regs_value))
0x17 --> (Schneider: read/write multiple registers) | (PyModbusTCP: ---)
0x43 --> (Schneider: read device ID)                | (PyModbusTCP: ---)
"""
try:
    plc = ModbusClient(host=ipPLC, auto_open=True, auto_close=True)
    plc.host(ipPLC)
    plc.port(portPLC)
    plc.open()

    if plc.is_open:
        writeRegister(13, 100)
except:
    writeRegister(13, 1)
    sys.exit()

############################################ MODBUS VERBINDUNG ENDE ####################################################

