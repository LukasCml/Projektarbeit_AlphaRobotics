"""
Funktion:     Ping Zeit Überwachung
Ersteller:    Lukas Camehl, Bernd Rensen, Jannik Birk
Datum:        03. Dezemeber 2021
Version:      Version 1.0
"""
import ping3
from Ablaufprogramme_Funktionen_CommunicationScript import *

def main():

    iprobot = "172.17.13.30"

    while True:
        response = ping3.ping(iprobot) * 1000
        response_gerundet = round(response, 2)
        writeRegister(24, response_gerundet)
        time.sleep(1)
        print(f"Die Reaktionszeit beträgt: {response_gerundet} ms")

if __name__ == "__main__":

    try:
        main()

    except:
        print("Es besteht keine Verbindung zum Roboter!!!")



