#Mathijs Schouten

#LIBRARIES
from tkinter import filedialog
import sys
import sqlite3
from random import randint
import time
import datetime

#VARIABELEN
d = datetime.datetime.now()
datum = "%s/%s/%s" %(d.day, d.month, d.year)
tijd = time.strftime("%X")

#SQL
kolomCasusNaam = 'casus_naam'
kolomOnderzoekerNaam = 'onderzoeker_naam'
intDataType = 'INTEGER'
floatDataType = 'REAL'
nullDataType = 'NULL'
textDataType = 'TEXT'
dataBlob = 'BLOB'

#FUNCTIE nieuwe casus
def nieuweCasus():

    casusNaam = str(input("Casus Naam: ")).replace(" ", "_")
    if(casusNaam == ""):
        casusNaam = ("BMMG_Casus_" + str(randint(0,99999999)))
        print("Casus Naam: " + casusNaam)

    onderzoekerNaam = str(input("Onderzoeker Naam: "))
    print("Welkom " + onderzoekerNaam + ". De casus is aangemaakt.")

    #databasebestand
    databaseBestand = casusNaam + ".sqlite"

    #connectie maken naar SQLite database
    connectie = sqlite3.connect(databaseBestand)
    #cursor object aanmaken
    c = connectie.cursor()

    #nieuwe database maken met casusnaam kolom
    c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'\
              .format(tabelnaam=casusNaam, kolomnaam=kolomCasusNaam, datatype=textDataType))

    #niewe kolommen toevoegen
    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"\
              .format(tabelnaam=casusNaam, kolomnaam=kolomOnderzoekerNaam, datatype=textDataType))

    #database vullen
    c.execute("INSERT INTO {tabelnaam} ({kolomnaam1}, {kolomnaam2}) VALUES ('{value1}', '{value2}')"\
              .format(tabelnaam=casusNaam, kolomnaam1=kolomCasusNaam, kolomnaam2=kolomOnderzoekerNaam, value1=casusNaam, value2=onderzoekerNaam))

    ##data opvragen uit de database en printen op scherm
    #c.execute('SELECT * FROM {tabelnaam}'. \
    #          format(tabelnaam=casusNaam))
    #dataUitDB = c.fetchall()
    #print(dataUitDB)

    #commit en close
    connectie.commit()
    connectie.close()

    ##imagebestand openen
    #print("Nieuwe Casus: Geef image-bestand op:")
    #imageBestand = filedialog.askopenfilename(filetypes=[(".img, .raw, .E01, etc..", ["*.img","*.raw"],)], title='Geef image-bestand op:')

    #if not imageBestand:
    #    sys.exit("Geen image-bestand geselecteerd, het programma wordt afgesloten")

    ##casus opslaglocatie
    #print("Geef aan waar u de casus wilt opslaan:")
    #opslagLocatie = filedialog.askdirectory(title='Geef aan waar u de casus wilt opslaan:')

#FUNCTIE bestaande casus
def bestaandeCasus():
    print("Bestaande Casus")

#MAIN CODE
print("Hallo, wat wilt u doen? \n")
print("Optie 1: Een nieuwe casus toevoegen")
print("Optie 2: Ga verder met een bestaande casus \n")

try:
    optie = int(input("Optie: "))
except ValueError:
    sys.exit("Geen optie opgegeven")

if(optie == 1):
    nieuweCasus()

elif(optie == 2):
    bestaandeCasus()