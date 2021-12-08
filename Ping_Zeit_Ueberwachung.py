"""
Funktion:     Ping Zeit Überwachung
Ersteller:    Lukas Camehl, Bernd Rensen, Jannik Birk
Datum:        03. Dezemeber 2021
Version:      Version 1.0
"""
import time
import ping3

pingListe = list()

def main():

    iprobot = "172.17.13.30"
    count = 0

    while count < 10:
        response = ping3.ping(iprobot) * 1000
        response_gerundet = round(response, 2)
        pingListe.append(response_gerundet)
        count = count + 1
        time.sleep(1)
        print(f"Die Reaktionszeit beträgt: {response_gerundet} ms")

    else:
        #eingabe = input("Wollen Sie den Durchschnitt berechnen?: ")
        #if eingabe == "ja":
        durschnitt = sum(pingListe)/len(pingListe)
        durschnitt_gerundet = round(durschnitt, 2)
        print(f"Der Durschnitt beträgt: {durschnitt_gerundet} ms")
        #if eingabe == "nein":
        main()

if __name__ == "__main__":

    try:
        main()

    except:
        print("Es besteht keine Verbindung zum Roboter!!!")



