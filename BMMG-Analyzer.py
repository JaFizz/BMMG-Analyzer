#Mathijs Schouten

#LIBRARIES
import tkFileDialog as filedialog
import sys
import sqlite3
from random import randint
import time
import datetime
import os
import pytsk3
import binascii
import hashlib

#VARIABELEN
d = datetime.datetime.now()
datum = "%s/%s/%s" %(d.day, d.month, d.year)
tijd = time.strftime("%X")

#Mappen
werkMap = "BMMG_Werkmap"
saveFileMap = "/savefile/"
extractsMap = "/extracts/"

#SQL Tabelnamen en Kolomnamen
kolomCasusNaam = 'casus_naam'
kolomOnderzoekerNaam = 'onderzoeker_naam'
kolomCasusMap = 'locatie_casusmap'

tabelImageBestand = "ImageBestand"
kolomImageNaam = "image_naam"
kolomImageLocatie = "image_locatie"

tabelFiles = 'Files'
kolomFileName = 'file_name'
kolomFileHash = 'file_md5_hash'
kolomFileExtension = 'file_extension'
kolomFileAccesTime = 'file_acces_time'
kolomFileModificationTime = 'file_modification_time'
kolomFileCreationTime = 'file_creation_time'
kolomFileExtractNameLocation = 'file_extract_name'

#kolomDataBLOB = 'data_blob'

#SQL datatypes
#intDataType = 'INTEGER'
#floatDataType = 'REAL'
#nullDataType = 'NULL'
textDataType = 'TEXT'
#dataBlob = 'BLOB'

#ENUMERATION van File Signatures
hexwaardes = {
    '4D5A' : 'EXE',
    '25504446' : 'PDF',
    'FFD8FFDB' : 'JPEG',
    'FFD8FFE0' : 'JPEG',
    'FFD8FFE1' : 'JPEG',
    '89504E470D0A1A0A' : 'PNG',
    '49492A00' : 'TIF',
    '4D4D002A' : 'TIFF',
    'D0CF11E0A1B11AE1' : 'COMPOUND',
    '464F524D' : 'TXT',
    '526172211A0700' : 'RAR',
    '526172211A070100' : 'RAR',
    '4B444D' : 'VMDK',
    '377ABCAF271C' : '7ZIP',
    '504B0304': 'ZIP',
    '504B0506': 'ZIP',
    '504B0708': 'ZIP'
}

#FUNCTIE nieuwe casus
def nieuweCasusToevoegen():
    print("\nEen nieuwe casus toevoegen")

    #casusnaam invoeren - foutafvanging moet nog
    casusNaam = raw_input(str("Geef Casus Naam (geen cijfer als eerste karakter): "))
    if not casusNaam:
        casusNaam = ("BMMG_Casus_" + str(randint(0,99999999)))
        print("Casus Naam: " + casusNaam)
    casusNaam = casusNaam.replace(" ", "_")

    #onderzoekernaam invoeren
    onderzoekerNaam = str(raw_input("Onderzoeker Naam: "))
    if not onderzoekerNaam:
        onderzoekerNaam = "Unknown"
        print("Onderzoeker Naam: "+onderzoekerNaam+"\n")

    #opslaglocatie laten kiezen
    opslagLocatie = filedialog.askdirectory(title='Geef aan in welke map u de casusbestanden wilt opslaan.'
                                                      '\nIn deze map worden de savefile en extracties opgeslagen')
    if not opslagLocatie:
        opslagLocatie = filedialog.askdirectory(title='Geef aan in welke map u de casusbestanden wilt opslaan.'
                                                          '\nIn deze map worden de savefile en extracties opgeslagen\n'
                                                          'Kies nu een map, anders wordt het programma afgesloten!')
        if not opslagLocatie:
            print "Geen opslaglocatie gekozen, er wordt een map aangemaakt in de map waarin het script staat...\n"

    ###mappen aanmaken
    #werkmap aanmaken in de opslaglocatie
    werkMapLocatie = (opslagLocatie+"/"+werkMap)
    if not os.path.exists(werkMapLocatie):
        os.makedirs(werkMapLocatie)
    #casusmap aanmaken in de werkmap
    casusMap = werkMapLocatie + "/" + casusNaam
    if not os.path.exists(casusMap):
        os.makedirs(casusMap)
    #savefilemap aanmaken in casusmap
    if not os.path.exists(casusMap + saveFileMap):
        os.makedirs(casusMap + saveFileMap)

    databaseBestandNaam = casusNaam + ".BMMG"

    #databasebestand maken in de savefilemap van de casusmap
    databaseBestand = casusMap + saveFileMap + databaseBestandNaam

    #connectie maken naar SQLite database
    connectie = sqlite3.connect(databaseBestand)

    #cursor object aanmaken
    c = connectie.cursor()

    #casusNaamInfo variable maken voor de database
    casusNaamInfo = casusNaam +"_info"

    #nieuwe tabel maken met casusnaam kolom
    c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=casusNaamInfo,
                                                                         kolomnaam=kolomCasusNaam, datatype=textDataType))

    #niewe kolommen toevoegen
    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
              .format(tabelnaam=casusNaamInfo, kolomnaam=kolomOnderzoekerNaam, datatype=textDataType))
    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
              .format(tabelnaam=casusNaamInfo, kolomnaam=kolomCasusMap, datatype=textDataType))

    #database vullen
    c.execute("INSERT INTO {tabelnaam} ({kolomnaam1}, {kolomnaam2}, {kolomnaam3}) VALUES ('{value1}', '{value2}', '{value3}')"
              .format(tabelnaam=casusNaamInfo, kolomnaam1=kolomCasusNaam, kolomnaam2=kolomOnderzoekerNaam,
                      kolomnaam3=kolomCasusMap, value1=casusNaam, value2=onderzoekerNaam, value3=casusMap))
    #commit
    connectie.commit()

    if onderzoekerNaam == "Unknown":
        print("Welkom! De casus is aangemaakt.\n"
              "De savefile: '" + databaseBestandNaam + "' is aangemaakt.\n"
                                             "De savefile is te vinden in de map: "+casusMap+saveFileMap+"\n"
                                                                                             "Met behulp van de savefile kunt u verdergaan met de casus wanneer u wilt.\n")
    else:
        print("Welkom " + onderzoekerNaam + "! De casus is aangemaakt.\n"
                                            "De savefile: '" + databaseBestandNaam + "' is aangemaakt.\n"
                                                                           "De savefile is te vinden in de map: "+casusMap+saveFileMap+"\n"
                                                                           "Met behulp van de savefile kunt u verdergaan met de casus wanneer u wilt.\n")

    #imagebestand openen
    print("Geef image-bestand op:")
    imageBestand = filedialog.askopenfilename(initialdir = "/",title = "Geef image-bestand op:",filetypes = (("E01","*.E01"),("all files","*.*")))
    if not imageBestand:
        imageBestand = filedialog.askopenfilename(initialdir = "/",title = "Geef image-bestand op:",filetypes = (("E01","*.E01"),("all files","*.*")))
        if not imageBestand:
            print "Twee keer geen imagebestand opgegeven, het programma wordt nu afgesloten"
            time.sleep(4)
            sys.exit()

    #imageName genereren
    imageName1 = os.path.splitext(os.path.basename(imageBestand))[0]
    extensie = os.path.splitext(imageBestand)[1]
    imageName = imageName1 + extensie
    print("\n"+imageName + " is toegevoegd aan de casus.\n")
    print "BMMG-Analyzer gaat nu bestanden extraheren, dit kan even duren...\n"
    time.sleep(5)

    #ImageBestand tabel maken
    c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=tabelImageBestand,
                                                                         kolomnaam=kolomImageNaam, datatype=textDataType))
    #ImageBestand kolom toevoegen
    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
              .format(tabelnaam=tabelImageBestand, kolomnaam=kolomImageLocatie, datatype=textDataType))

    #ImageBestand tabel vullen
    c.execute("INSERT INTO {tabelnaam} ({kolomnaam1},{kolomnaam2}) VALUES ('{value1}','{value2}')"
              .format(tabelnaam=tabelImageBestand, kolomnaam1=kolomImageNaam, kolomnaam2=kolomImageLocatie, value1=imageName, value2=imageBestand))
    #commit
    connectie.commit()

    #werkmap aanmaken in de opslaglocatie
    extractsLocatie = (casusMap+extractsMap)
    if not os.path.exists(extractsLocatie):
        os.makedirs(extractsLocatie)

    #Naar Extractfunctie()
    extractor(casusNaam, connectie, c, imageBestand, extractsLocatie)

#FUNCTIE bestaande casus
def bestaandeCasusOpenen():
    print("\nEen bestaande casus openen")

    #databasebestand laten kiezen
    databaseBestand = filedialog.askopenfilename(initialdir = "/",title = "Open een bestaande casus(.BMMG-extensie):",filetypes = (("BMMG-Casus","*.BMMG"),))
    if not databaseBestand:
        databaseBestand = filedialog.askopenfilename(initialdir = "/",title = "Open een bestaande casus:",filetypes = (("BMMG-Casus","*.BMMG"),))
        if not databaseBestand:
            print "Twee keer geen savefile opgegeven, het programma wordt afgesloten"
            time.sleep(5)
            sys.exit()

    #bestandsextensie verwijderen van de bestandsnaam om zo casusnaaminfo te maken die nodig is in de database
    casusNaam = os.path.basename(databaseBestand[:-5])
    casusNaamInfo = casusNaam +"_info"

    #connectie maken naar SQLite database
    connectie = sqlite3.connect(databaseBestand)

    #cursor object aanmaken
    c = connectie.cursor()

    #data opvragen uit de database en printen op scherm
    c.execute('SELECT * FROM {tabelnaam}'. \
              format(tabelnaam=casusNaamInfo))
    dataUitDB = c.fetchone()[0]
    print("\nDe casus: '"+ dataUitDB + "' is geopend.")
    print "U wordt doorgestuurd naar het werkmenu..."
    time.sleep(5)

    #imagebestandlocatie opvragen uit database
    c.execute('SELECT image_locatie FROM ImageBestand')
    imageBestand = c.fetchone()[0]

    #commit
    connectie.commit()

    #Naar het werkmenu
    werkMenu(casusNaam, connectie, c, imageBestand)

def extractor(casusNaam, connectie, c, imageBestand, extractsLocatie):
    casusNaam = casusNaam
    connectie = connectie

    try:
        #Files tabel maken
        c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=tabelFiles,
                                                                             kolomnaam=kolomFileName, datatype=textDataType))
        #Nieuwe kolommen toevoegen
        c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                  .format(tabelnaam=tabelFiles, kolomnaam=kolomFileExtractNameLocation, datatype=textDataType))
        c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                  .format(tabelnaam=tabelFiles, kolomnaam=kolomFileHash, datatype=textDataType))
        c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                  .format(tabelnaam=tabelFiles, kolomnaam=kolomFileExtension, datatype=textDataType))
        c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                  .format(tabelnaam=tabelFiles, kolomnaam=kolomFileCreationTime, datatype=textDataType))
        c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                  .format(tabelnaam=tabelFiles, kolomnaam=kolomFileModificationTime, datatype=textDataType))
        c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                  .format(tabelnaam=tabelFiles, kolomnaam=kolomFileAccesTime, datatype=textDataType))
        #commit
        connectie.commit()

        #imagebestand in een andere variabele zetten
        imageFile = imageBestand
        #image handle aanmaken voor het imagebestand
        image = pytsk3.Img_Info(imageFile)

        #Loop door een mapje
        def checkDirectory(handle):
            #voor alles wat ik tegenkom
            for file in handle:
                #als het begint met een . of .. -> ga door naar volgende
                if file.info.name.name in [".", ".."]:
                    continue

                else:
                    try:
                        #meta type vaststellen met pytsk
                        ftype = file.info.meta.type
                        #Als er een mapje is gevonden
                        if ftype == pytsk3.TSK_FS_META_TYPE_DIR:
                            #print "Map gevonden ---> wordt nu gecheckt"
                            #geef directory naam mee aan functie om te doorzoeken
                            checkDirectory(file.as_directory())

                        #Als er een bestand is gevonden
                        else:
                            #lees eerste 16 bytes van de file (header bytes)
                            header_bytes = file.read_random(0, 16)
                            #maak hexwaarde van de header_bytes, maakt ze ook hoofdletters
                            hexwaarde = binascii.hexlify(header_bytes).upper()

                            #Extract functie
                            def extract(filename):
                                filename1 = os.path.splitext(filename)[0]
                                #random integer voor de filename filename
                                filename2 =  str(randint(0,99999999)) + "_" + filename1
                                #extensie splitten van filename
                                extensie = os.path.splitext(filename)[1]
                                #bestandlocatie genereren met extractslocatie + filename
                                extractName = extractsLocatie + filename2 + extensie

                                #bestand wegschrijven
                                bestand = open(extractName, 'w')
                                bestand.write(file.read_random(0, file.info.meta.size))
                                bestand.close()
                                print "\n\n-----------------------------------------FILE---------------------------------------------------"
                                print filename + " extracted.\nFiledirectory: " + extractName
                                print "---------------------------------------"+tijd+"------------------------------------BMMG-Analyzer\n"

                                #MD5 hashwaarde berekenen
                                hashValue =  hashlib.md5(open(extractName, 'rb').read()).hexdigest()
                                return extensie, hashValue, extractName

                            #kijk of hexwaarde in fileheader voorkomt
                            for waarde in hexwaardes:
                                if waarde in hexwaarde:
                                    #filename
                                    filename = file.info.name.name
                                    #access time
                                    accesTime = file.info.meta.atime
                                    #modification time
                                    modificationTime = file.info.meta.mtime
                                    #creation time
                                    creationTime = file.info.meta.crtime

                                    # extensie en hashvalue en extractname zijn returnvalues van extract
                                    extensie, hashValue, extractName = extract(filename)

                                    #ImageBestand tabel vullen
                                    c.execute("INSERT INTO {tabelnaam} ({kolomnaam1},{kolomnaam2},{kolomnaam3},{kolomnaam4},{kolomnaam5},{kolomnaam6},{kolomnaam7})"
                                    " VALUES ('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}','{value7}')"
                                    .format(tabelnaam=tabelFiles, kolomnaam1=kolomFileName, kolomnaam2=kolomFileExtension, kolomnaam3=kolomFileHash,
                                            kolomnaam4=kolomFileAccesTime, kolomnaam5=kolomFileModificationTime, kolomnaam6=kolomFileCreationTime, kolomnaam7=kolomFileExtractNameLocation,
                                            value1=filename, value2=extensie, value3=hashValue, value4=accesTime, value5=modificationTime, value6=creationTime, value7=extractName))
                                    #commit
                                    connectie.commit()
                    except:
                        #Geen map of bestand gevonden
                        continue

        #Partitie tabel ophalen met behulp van de handle
        partitionTable = pytsk3.Volume_Info(image)
        #blocksize ophalen
        bsize = partitionTable.info.block_size

        #directory checker
        for part in partitionTable:
            #print part
            try:
                partitionHandle = pytsk3.FS_Info(image, offset=(part.start * bsize))
                handle = partitionHandle.open_dir(path='/')
                checkDirectory(handle)
            except IOError as error:
                #error == Unable to open the image as a filesystem: Cannot determine file system type
                print ">>>>>>>>>>>>>>"

    except:
        print "Extractie succesvol, u wordt doorgestuurd naar het werkmenu..."
    time.sleep(5)
    werkMenu(casusNaam, connectie, c, imageBestand)

def werkMenu(casusNaam, connectie, c, imageBestand):

    print ("\n" * 35)
    print("\nWerkmenu:\n")

    #casusnaaminfo maken voor de database
    casusNaamInfo = casusNaam+"_info"

    #Werkmenu opties printen op scherm
    print("Optie 1: Casusnaam opvragen")
    print("Optie 2: ")
    print("Optie 3: BMMG-Analyzer afsluiten")

    #optie kiezen in het werkmenu
    try:
        optie = raw_input("\nKies een optie: ")
        if not optie:
            optie = raw_input("\nKies een optie. Vul een optie van hierboven in!!!: ")
            if not optie:
                optie = raw_input("\nKies een optie. Vul een optie van hierboven in!!!: ")
                print ("Twee keer geen optie opgegeven, het programma wordt afgesloten")
                time.sleep(3)
                sys.exit()
    except ValueError:
        optie = raw_input("\nKies een optie. Vul een optie van hierboven in!!!: ")
        if not optie:
            optie = raw_input("\nKies een optie. Vul een optie van hierboven in!!!: ")
            print ("Twee keer geen optie opgegeven, het programma wordt afgesloten")
            time.sleep(3)
            sys.exit()




    if(optie == 1):
    #casusnaam opvragen uit de database en printen op scherm
        c.execute('SELECT casus_naam FROM {tabelnaam}'
                  .format(tabelnaam=casusNaamInfo))
        dataUitDB = c.fetchone()
        print("\nCasus Naam: "+(dataUitDB[0]))

        #weer naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    if(optie == 2):
        print "leeg"

    if(optie == 3):
        print "Het programma wordt over 3 seconden afgesloten..."
        connectie.close()
        time.sleep(3)
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
print("Optie 2: Een bestaande casus openen\n")

#optie kiezen aan begin van programma

try:
    optie = int(raw_input("Kies een optie: "))
except:
    try:
        optie = int(raw_input("Kies een optie. Vul een cijfer in !!! "))
    except:
        print("Twee keer geen optie opgegeven, het programma wordt afgesloten.")
        time.sleep(5)
        sys.exit()

#doorsturen naar gekozen optie
if(optie == 1):
    nieuweCasusToevoegen()

elif(optie == 2):
    bestaandeCasusOpenen()