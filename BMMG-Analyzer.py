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
import pyewf
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
kolomFileSymbolicLink = 'file_symbolic_link'

#SQL datatypes
#kolomDataBLOB = 'data_blob'
#intDataType = 'INTEGER'
#floatDataType = 'REAL'
#nullDataType = 'NULL'
textDataType = 'TEXT'
#dataBlob = 'BLOB'

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
        try:
            opslagLocatie = filedialog.askdirectory(title='Geef aan in welke map u de casusbestanden wilt opslaan.'
                                                          '\nIn deze map worden de savefile en extracties opgeslagen\n'
                                                          'Kies nu een map, anders wordt het programma afgesloten!')
        except:
            print "Twee keer geen opslaglocatie gekozen, het programma wordt afgesloten"
            time.sleep(5)
            sys.exit()

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
    #imageBestand = filedialog.askopenfilename(filetypes=[(".img, .raw, .E01, etc.."), ["*.img","*.raw","*.E01","*.e01","*.dd"]], title='Geef image-bestand op:')
    imageBestand = filedialog.askopenfilename(initialdir = "/",title = "Geef image-bestand op:",filetypes = (("E01","*.E01"),("all files","*.*")))
    if not imageBestand:
        try:
            imageBestand = filedialog.askopenfilename(initialdir = "/",title = "Geef image-bestand op:",filetypes = (("E01","*.E01"),("all files","*.*")))
        except:
            print("Twee keer geen image-bestand geselecteerd, het programma wordt afgesloten")
            time.sleep(5)
            sys.exit()
    #imageName genereren
    imageName1 = os.path.splitext(os.path.basename(imageBestand))[0]
    extensie = os.path.splitext(imageBestand)[1]
    imageName = imageName1 + extensie
    print("\n"+imageName + " is toegevoegd aan de casus.")

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

    #Naar werkMenu()
    werkMenu(casusNaam, connectie, c, imageBestand)

#FUNCTIE bestaande casus
def bestaandeCasusOpenen():
    print("\nOpen een bestaande casus")

    #databasebestand
    #databaseBestand = filedialog.askopenfilename(filetypes=[(".BMMG", ["*.BMMG"],)], title='Open een bestaande casus:')
    databaseBestand = filedialog.askopenfilename(initialdir = "/",title = "Open een bestaande casus:",filetypes = (("BMMG-File","*.BMMG"),))

    if not databaseBestand:
        try:
            databaseBestand = filedialog.askopenfilename(initialdir = "/",title = "Open een bestaande casus:",filetypes = (("BMMG-File","*.BMMG"),))
        except:
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

    #imagebestandlocatie opvragen uit database
    c.execute('SELECT image_locatie FROM ImageBestand')
    imageBestand = c.fetchone()[0]

    #commit
    connectie.commit()

    #Naar het werkmenu
    werkMenu(casusNaam, connectie, c, imageBestand)

def extractor(casusNaam, connectie, c, imageBestand):
    casusNaam = casusNaam
    connectie = connectie
    c = c

    # imagebestand
    imageFile = imageBestand
    # image handle
    imagehandle = pytsk3.Img_Info(imageFile)

    def checkDirectory(handle):
        for file in handle:
            if file.info.name.name in [".", ".."]:
                continue

            else:
                try:
                    ftype = file.info.meta.type
                    # Mapje gevonden
                    if ftype == pytsk3.TSK_FS_META_TYPE_DIR:
                        print "MAP GEVONDEN !!!"
                        #print directory naam
                        #print file.info.name.name
                        #geef directory naam mee aan functie om te doorzoeken
                        checkDirectory(file.as_directory())

                    # Bestand gevonden, doe er iets mee
                    else:
                        header_bytes = file.read_random(0, 16)
                        hexwaarde = binascii.hexlify(header_bytes).upper()

                        exehex = '4D5A'
                        pdfhex = '25504446'
                        jpeghex = 'FFD8FFDB'  # jpeg
                        jpeghex1 = 'FFD8FFE0'  # jpeg
                        jpeghex2 = 'FFD8FFE1'  # jpeg
                        pnghex1 = '89504E470D0A1A0A' #png
                        tifhex = '49492A00'  # tif
                        tiffhex = '4D4D002A'  # tiff
                        compoundhex = 'D0CF11E0A1B11AE1'  # Compounds, doc, xls, ppt
                        txthex = '464F524Dnnnnnnnn46545854'  # txt

                        def extract(filename):
                            bestand = open(filename, 'w')
                            bestand.write(file.read_random(0, file.info.meta.size))
                            bestand.close()

                        #                    os.makedirs('/exports/')
                        #kijk of hexwaarde in fileheader voorkomt
                        if exehex in hexwaarde:
                            #print file.info.name.name + ' = een executable'
                            filename = file.info.name.name
                            extract(filename)

                        if pdfhex in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if jpeghex in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if jpeghex1 in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if jpeghex2 in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if pnghex1 in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if tiffhex in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if tifhex in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if compoundhex in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)

                        if txthex in hexwaarde:
                            filename = file.info.name.name
                            extract(filename)


                except:
                    print ""


    # partitie table
    partitionTable = pytsk3.Volume_Info(imagehandle)
    bsize = partitionTable.info.block_size

    for part in partitionTable:
        print part
        try:
            partitionHandle = pytsk3.FS_Info(imagehandle, offset=(part.start * bsize))
            directoryHandle = partitionHandle.open_dir(path='/')
            checkDirectory(directoryHandle)
        except IOError as error:
            print ""

#def extractor(casusNaam, connectie, c, imageBestand, extractsLocatie):
#    casusNaam = casusNaam
#    connectie = connectie
#
#    #Files tabel maken
#    c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=tabelFiles,
#                                                                         kolomnaam=kolomFileName, datatype=textDataType))
#    #Nieuwe kolommen toevoegen
#    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
#              .format(tabelnaam=tabelFiles, kolomnaam=kolomFileHash, datatype=textDataType))
#    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
#              .format(tabelnaam=tabelFiles, kolomnaam=kolomFileExtension, datatype=textDataType))
#    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
#              .format(tabelnaam=tabelFiles, kolomnaam=kolomFileAccesTime, datatype=textDataType))
#    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
#              .format(tabelnaam=tabelFiles, kolomnaam=kolomFileModificationTime, datatype=textDataType))
#    c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
#              .format(tabelnaam=tabelFiles, kolomnaam=kolomFileCreationTime, datatype=textDataType))
#
#    #commit
#    connectie.commit()
#
#    class EwfImgInfo(pytsk3.Img_Info):
#        def __init__(self, ewf_handle):
#                self._ewf_handle = ewf_handle
#                super(EwfImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
#
#    #imagebestand
#    imageFile = imageBestand
#    #image handle
#    image = pytsk3.Img_Info(imageFile)
#
#    #Loop door een mapje
#    def checkDirectory(handle):
#
#        for file in handle:
#
#            if file.info.name.name in [".", ".."]:
#                continue
#            else:
#                try:
#                    ftype = file.info.meta.type
#                    #Als er een mapje is gevonden
#                    if ftype == pytsk3.TSK_FS_META_TYPE_DIR:
#                        print "Map gevonden"
#                        #print directory naam
#                        #print file.info.name.name
#                        #geef directory naam mee aan functie om te doorzoeken
#                        checkDirectory(file.as_directory())
#
#                    #Als er een bestand is gevonden
#                    else:
#                        #lees eerste 16 bytes van de file (header bytes)
#                        header_bytes = file.read_random(0, 16)
#                        #maak hexwaarde van de header_bytes, maakt ze ook hoofdletters
#                        hexwaarde = binascii.hexlify(header_bytes).upper()
#
#                        print hexwaarde
#
#                        #ENUMERATION van File Signatures
#                        hexwaardes = {
#                            '4D5A' : 'EXE',
#                            '25504446' : 'PDF',
#                            'FFD8FFDB' : 'JPEG',
#                            'FFD8FFE0' : 'JPEG',
#                            'FFD8FFE1' : '',
#                            '89504E470D0A1A0A' : 'PNG',
#                            '49492A00' : 'TIF',
#                            '4D4D002A' : 'TIFF',
#                            'D0CF11E0A1B11AE1' : 'COMPOUND',
#                            '464F524D' : 'TXT',
#                            '526172211A0700' : 'RAR',
#                            '526172211A070100' : 'RAR',
#                            '4B444D' : 'VMDK',
#                            '377ABCAF271C' : '7ZIP',
#                            '504B0304': 'ZIP',
#                            '504B0506': 'ZIP',
#                            '504B0708': 'ZIP'
#                        }
#
#                        print hexwaardes
#
#                        #Extract functie
#                        def extract(filename):
#                            bestand = open(filename, 'w')
#                            bestand.write(file.read_random(0, file.info.meta.size))
#                            bestand.close()
#
#                            ##1 Filename
#                            ##is al meegegeven in de functie
#                            ##2 hashwaarde MD5
#                            ##pas berekenen na het extracten van de image
#                            ##3 file extensie
#                            #extensie = os.path.splitext(filename)[1]
#                            ##4 access time
#                            #accesTime = file.info.meta.atime
#                            #accesTime = accesTime.astype("datetime64[s]")
#                            ##5 modification time
#                            #modificationTime = file.info.meta.mtime
#                            ##6 creation time
#                            #creationTime = file.info.meta.crtime
#
#                            #print filename
#                            #print extensie
#                            #print accesTime
#                            #print modificationTime
#                            #print creationTime
#
#                            ##extractslocatie + filename genereren
#                            #bestandLocatie = extractsLocatie + filename
#                            ##file aanmaken met write rechten
#                            #bestand = open(bestandLocatie, 'rw')
#                            ###file wegschrijven
#                            #bestand.write(file.read_random(0, file.info.meta.size))
#
#                            ##MD5 hashwaarde berekenen
#                            #hashwaardeMD5 = hashlib.md5(bestand).hexdigest()
#
#                            #bestand.close()
#                            #print filename+" extracted"
#
#                            ##ImageBestand tabel vullen
#                            #c.execute("INSERT INTO {tabelnaam} ({kolomnaam1},{kolomnaam2},{kolomnaam3},{kolomnaam4},{kolomnaam5},{kolomnaam6})"
#                            #          " VALUES ('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}')"
#                            #          .format(tabelnaam=tabelImageBestand, kolomnaam1=kolomFileName, kolomnaam2=kolomFileHash, kolomnaam3=kolomFileExtension, kolomnaam4=kolomFileAccesTime, kolomnaam5=kolomFileModificationTime, kolomnaam6=kolomFileCreationTime, value1=filename, value2=hashwaardeMD5, value3=extensie, value4=accesTime, value5=modificationTime, value6=creationTime))
#
#                            ##commit
#                            #connectie.commit()
#                        #kijk of hexwaarde in fileheader voorkomt
#                        for waarde in hexwaardes:
#                            if waarde in hexwaarde:
#                                filename = file.info.name.name
#                                extract(filename)
#
#                except:
#                    print "Geen directory of bestand"
#
#    #Partitie tabel ophalen met behulp van de handle
#    partitionTable = pytsk3.Volume_Info(image)
#    #blocksize ophalen
#    bsize = partitionTable.info.block_size
#
#    #directory checker
#    for part in partitionTable:
#        print part
#        try:
#            partitionHandle = pytsk3.FS_Info(image, offset=(part.start * bsize))
#            directoryHandle = partitionHandle.open_dir(path='/')
#            checkDirectory(directoryHandle)
#        except IOError as error:
#            print "Error"

def werkMenu(casusNaam, connectie, c, imageBestand):

    print("\nWerkmenu:\n")

    #casusnaaminfo maken voor de database
    casusNaamInfo = casusNaam+"_info"

    #locatie casusmap opvragen uit database
    c.execute('SELECT locatie_casusmap FROM {tabelnaam}'. \
              format(tabelnaam=casusNaamInfo))
    locatieCasusMap = c.fetchone()[0]

    #werkmap aanmaken in de opslaglocatie
    extractsLocatie = (locatieCasusMap+extractsMap)
    if not os.path.exists(extractsLocatie):
        os.makedirs(extractsLocatie)

    #Werkmenu opties
    print("Optie 1: Casusnaam opvragen")
    print("Optie 2: Files extraheren")
    print("Optie 3: BMMG-Analyzer afsluiten")

    #optie kiezen
    optie = int(raw_input("\nKies een optie: "))
    if not optie:
        try:
            optie = int(raw_input("\nKies een optie. Vul een cijfer in!!!: "))
        except ValueError:
            sys.exit("Twee keer geen optie opgegeven, het programma wordt afgesloten")



    if(optie == 1):
    #casusnaam opvragen uit de database en printen op scherm
        c.execute('SELECT casus_naam FROM {tabelnaam}'
                  .format(tabelnaam=casusNaamInfo))
        dataUitDB = c.fetchone()
        print("\nCasus Naam: "+(dataUitDB[0]))

        #weer naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    if(optie == 2):

        extractor(casusNaam, connectie, c, imageBestand)

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
print("Optie 2: Ga verder met een bestaande casus \n")

#optie kiezen
optie = int(raw_input("Kies een optie: "))
if not optie:
    try:
        optie = int(raw_input("Kies een optie. Vul een cijfer in!!! "))
    except:
        print("Twee keer geen optie opgegeven, het programma wordt afgesloten.")
        time.sleep(5)
        sys.exit()

#doorsturen naar gekozen optie
if(optie == 1):
    nieuweCasusToevoegen()

elif(optie == 2):
    bestaandeCasusOpenen()