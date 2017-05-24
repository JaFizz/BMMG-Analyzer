#Mathijs Schouten

#imports
from tkinter import filedialog
import sys

#functies

#nieuwe casus
def nieuweCasus():
    print("New Case:")
    imageBestand = filedialog.askopenfilename(filetypes=((".img, .raw, .E01, etc..", ["*.img","*.raw"]), ))

    if not imageBestand:
        sys.exit("Geen image-bestand geselecteerd, het programma wordt afgesloten")

    casusNaam = str(input("Geef een casusnaam op: "))
    onderzoekerNaam = str(input("Geef onderzoeker naam op: "))


#bestaande casus
def bestaandeCasus():
    print("Existing Case")


#Main Code
print("Hallo, wat wilt u doen? \n")
print("Optie 1: Nieuwe casus")
print("Optie 2: Bestaande casus \n")

try:
    optie = int(input("Optie: "))
except ValueError:
    sys.exit("Geen optie opgegeven")

if(optie == 1):
    nieuweCasus()

elif(optie == 2):
    bestaandeCasus()