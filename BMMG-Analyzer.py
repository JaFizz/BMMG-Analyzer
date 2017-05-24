#Mathijs Schouten

#imports
from tkinter import filedialog
import sys
import sqlite3

#functies

#nieuwe casus
def nieuweCasus():
    #imageBestand openen
    print("Nieuwe Casus: Geef image-bestand op:")
    imageBestand = filedialog.askopenfilename(filetypes=[(".img, .raw, .E01, etc..", ["*.img","*.raw"],)], title='Geef image-bestand op:')

    #foutafvanging
    if not imageBestand:
        sys.exit("Geen image-bestand geselecteerd, het programma wordt afgesloten")

    #casus details
    casusNaam = str(input("Geef een casusnaam op: "))
    onderzoekerNaam = str(input("Geef onderzoeker naam op: "))

    #casus opslaglocatie
    print("Geef aan waar u de casus wilt opslaan:")
    opslagLocatie = filedialog.askdirectory(title='Geef aan waar u de casus wilt opslaan:')

    #databasebestand
    databaseBestand = str(input("Vul een naam in voor het opslagbestand: "))

    #connectie maken naar SQLite database
    conn = sqlite3.connect(databaseBestand)
    c = conn.cursor()

    #nieuwe database maken
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
              .format(tn=casusNaam, nf='casusNaam', ft='TEXT'))

    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".\
            format(tn=casusNaam, cn='onderzoeker_column', ct='TEXT'))

    c.execute("INSERT INTO {tn} ({idf}), {cn}) VALUES ('test')".\
              format(tn=casusNaam, idf='onderzoeker_column', cn='onderzoeker_column'))

    c.execute('SELECT * FROM {tn}'.\
              format(tn=casusNaam))

    allerijen = c.fetchall()
    print(allerijen)
    conn.commit()
    conn.close()

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