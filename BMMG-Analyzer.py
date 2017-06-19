#Mathijs Schouten

#LIBRARIES
from tkinter import filedialog
import sys
import sqlite3
from random import randint
import time
import datetime
import os

#VARIABELEN
d = datetime.datetime.now()
datum = "%s/%s/%s" %(d.day, d.month, d.year)
tijd = time.strftime("%X")

#SQL
kolomCasusNaam = 'casus_naam'
kolomOnderzoekerNaam = 'onderzoeker_naam'
#kolomDataBLOB = 'data_blob'
#intDataType = 'INTEGER'
#floatDataType = 'REAL'
#nullDataType = 'NULL'
textDataType = 'TEXT'
#dataBlob = 'BLOB'

#FUNCTIE nieuwe casus
def nieuweCasusToevoegen():

    print("\nEen nieuwe casus toevoegen")

    #casusnaam invoeren - foutafvanging moet nog ingevoerd worden
    casusNaam = input("Casus Naam: ").replace(" ", "_")
    if(casusNaam == ""):
        casusNaam = ("BMMG_Casus_" + str(randint(0,99999999)))
        print("Casus Naam: " + casusNaam)

    onderzoekerNaam = str(input("Onderzoeker Naam: "))

    #databasebestand
    databaseBestand = casusNaam + ".BMMG"

    #connectie maken naar SQLite database
    connectie = sqlite3.connect(databaseBestand)

    #cursor object aanmaken
    c = connectie.cursor()

    casusNaamInfo = casusNaam +"_info"

    #nieuwe tabel maken met casusnaam kolom
    c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'\
              .format(tabelnaam=casusNaamInfo, kolomnaam=kolomCasusNaam, datatype=textDataType))

    #niewe kolommen toevoegen
    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"\
              .format(tabelnaam=casusNaamInfo, kolomnaam=kolomOnderzoekerNaam, datatype=textDataType))

    #database vullen
    c.execute("INSERT INTO {tabelnaam} ({kolomnaam1}, {kolomnaam2}) VALUES ('{value1}', '{value2}')"\
              .format(tabelnaam=casusNaamInfo, kolomnaam1=kolomCasusNaam, kolomnaam2=kolomOnderzoekerNaam, value1=casusNaam, value2=onderzoekerNaam))

    #commit
    connectie.commit()

    print("Welkom " + onderzoekerNaam + ". De casus is aangemaakt. De savefile: '" + databaseBestand + "' is aangemaakt.")

    #imagebestand openen
    print("Geef image-bestand op:")
    imageBestand = filedialog.askopenfilename(filetypes=[(".img, .raw, .E01, etc..", ["*.img","*.raw","*.txt","*.mp3"],)], title='Geef image-bestand op:')

    if not imageBestand:
        print("Geen image-bestand geselecteerd, het programma wordt afgesloten")
        time.sleep(5)
        sys.exit()

    imageName1 = os.path.splitext(os.path.basename(imageBestand))[0]
    extensie = os.path.splitext(imageBestand)[1]
    imageName = imageName1 + extensie
    print("\n"+imageName + " is toegevoegd aan de casus.")

    #ImageBestand tabel maken
    c.execute("CREATE TABLE ImageBestand (image_naam TEXT NOT NULL PRIMARY KEY, image_bestand BLOB NOT NULL);")

    imageBestandOpen = open(imageBestand, 'rb').read()

    c.execute("INSERT INTO ImageBestand (image_naam, image_bestand) values (?, ?)",
              (imageName, sqlite3.Binary(imageBestandOpen)))
    connectie.commit()

    werkMenu(casusNaam, connectie, c)

#FUNCTIE bestaande casus
def bestaandeCasusOpenen():
    print("\nOpen een bestaande casus")

    #databasebestand
    databaseBestand = filedialog.askopenfilename(filetypes=[(".BMMG", ["*.BMMG"],)], title='Open een bestaande casus:')

    #bestandsextensie verwijderen van de bestandsnaam
    casusNaam = os.path.basename(databaseBestand[:-5])

    #connectie maken naar SQLite database
    connectie = sqlite3.connect(databaseBestand)

    #cursor object aanmaken
    c = connectie.cursor()

    casusNaamInfo = casusNaam +"_info"

    #data opvragen uit de database en printen op scherm
    c.execute('SELECT * FROM {tabelnaam}'. \
              format(tabelnaam=casusNaamInfo))
    dataUitDB = c.fetchone()[0]
    print("\nDe casus: '"+ dataUitDB + "' is geopend.")

    #commit
    connectie.commit()

    werkMenu(casusNaam, connectie, c)

def werkMenu(casusNaam, connectie, c):

    print("\nWerkmenu:\n")

    #Werkmenu opties
    print("Optie 1: Casusinformatie opvragen")
    print("Optie 2: Bestand wegschrijven")
    print("Optie 3: BMMG-Analyzer afsluiten")

    try:
        optie = int(input("\nKies een optie: "))
    except ValueError:
        sys.exit("Geen optie opgegeven")

    casusNaamInfo = casusNaam+"_info"

    if(optie == 1):
    #casusinformatie opvragen uit de database en printen op scherm
        c.execute('SELECT casus_naam FROM {tabelnaam}'. \
              format(tabelnaam=casusNaamInfo))
        dataUitDB = c.fetchone()
        print("\nCasus Naam: "+(dataUitDB[0]))

        werkMenu(casusNaam, connectie, c)

    if(optie == 2):
        c.execute('SELECT image_naam FROM ImageBestand')
        imageNaam = c.fetchone()[0]

        #opslaglocatie
        print("Waar wilt u het imagebestand opslaan?")
        opslagLocatie = filedialog.askdirectory(title='Geef aan waar u het imagebestand wilt opslaan:')

        with open(opslagLocatie+"\\"+imageNaam, 'wb') as imageBestand:
            c.execute('SELECT image_bestand FROM ImageBestand')
            ablob = c.fetchone()
            imageBestand.write(ablob[0])

    #    try:
        print("\nImagebestand is weggeschreven")
    #    except IOError:
    #        print("Geen imagebestand weggeschreven")

        werkMenu(casusNaam, connectie, c)

    if(optie == 3):
        connectie.close()
        sys.exit()

#MAIN CODE
print(
" ____   __  __  __  __   _____                                _                        \n"
"|  _ \ |  \/  ||  \/  | / ____|          /\                  | |                       \n"
"| |_) || \  / || \  / || |  __  ______  /  \    _ __    __ _ | | _   _  ____ ___  _ __ \n"
"|  _ < | |\/| || |\/| || | |_ ||______|/ /\ \  | '_ \  / _` || || | | ||_  // _ \| '__|\n"
"| |_) || |  | || |  | || |__| |       / ____ \ | | | || (_| || || |_| | / /|  __/| |   \n"
"|____/ |_|  |_||_|  |_| \_____|      /_/    \_\|_| |_| \__,_||_| \__, |/___|\___||_|   \n"
"                                                                  __/ |                \n"
"                                                                 |___/ "+datum+" "+tijd+" \n"
"===========================================================================================\n"
)

print("Goedendag, wat wilt u doen? \n")
print("Optie 1: Een nieuwe casus toevoegen")
print("Optie 2: Ga verder met een bestaande casus \n")

try:
    optie = int(input("Kies een optie: "))
except ValueError:
    sys.exit("Geen optie opgegeven")

if(optie == 1):
    nieuweCasusToevoegen()

elif(optie == 2):
    bestaandeCasusOpenen()