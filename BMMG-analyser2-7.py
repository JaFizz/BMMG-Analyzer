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
#import md5
#from hashlib import md5
#import pyewf
from termcolor import colored
import csv

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

def extractor(casusNaam, connectie, c, imageBestand, extractsLocatie):
    casusNaam = casusNaam
    connectie = connectie

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

    #class EwfImgInfo(pytsk3.Img_Info):
    #    def __init__(self, ewf_handle):
    #            self._ewf_handle = ewf_handle
    #            super(EwfImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    #imagebestand
    imageFile = imageBestand
    #image handle
    image = pytsk3.Img_Info(imageFile)

    #Loop door een mapje
    def checkDirectory(handle):

        for file in handle:

            if file.info.name.name in [".", ".."]:
                continue

            else:

                try:
                    ftype = file.info.meta.type
                    #Als er een mapje is gevonden

                    if ftype == pytsk3.TSK_FS_META_TYPE_DIR:
                        #print "Map gevonden ---> wordt nu gecheckt"
                        #geef directory naam mee aan functie om te doorzoeken
                        checkDirectory(file.as_directory())

                    #Als er een bestand is gevonden
                    else:
                        #print "Bestand:\n"
                        #lees eerste 16 bytes van de file (header bytes)
                        header_bytes = file.read_random(0, 16)
                        #maak hexwaarde van de header_bytes, maakt ze ook hoofdletters
                        hexwaarde = binascii.hexlify(header_bytes).upper()

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

                        #Extract functie
                        def extract(filename):
                            filename1 = os.path.splitext(filename)[0]
                            #random integer voor de filename filename
                            filename2 =  str(randint(0,99999999)) + "_" + filename1

                            print "Stap:" + filename2

                            extensie = os.path.splitext(filename)[1]

                            #bestandlocatie genereren met extractslocatie + filename
                            extractName = extractsLocatie + filename2 + extensie

                            bestand = open(extractName, 'w')
                            bestand.write(file.read_random(0, file.info.meta.size))
                            bestand.close()
                            print filename + " extracted.\nFiledirectory: " + extractName
                            print "-------------------------------------------------------------------------------------\n"

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
                                #print "Commit"

                except:
                    #print "Geen map of bestand gevonden"
                    continue

    #Partitie tabel ophalen met behulp van de handle
    partitionTable = pytsk3.Volume_Info(image)
    #blocksize ophalen
    bsize = partitionTable.info.block_size

    #directory checker
    for part in partitionTable:
        print part
        try:
            partitionHandle = pytsk3.FS_Info(image, offset=(part.start * bsize))
            handle = partitionHandle.open_dir(path='/')
            checkDirectory(handle)
        except IOError as error:
            print "-----------"
            #werkMenu(casusNaam, connectie, c, imageBestand)

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
    print("Optie 2: Extractie van Image bestand")
    print("Optie 3: BMMG-Analyzer afsluiten \n ")
    print colored('LET OP! Optie 4 t/m Optie 25 kunnen pas gekozen worden zodra Optie 2 is uitgevoerd. \n', 'red' )
    print("Optie 4: Extractie van combound bestanden uit image bestand")
    print("Optie 5: Extractie van tekst uit bestanden uit image bestand")
    print("Optie 6: Extractie van metadata uit bestanden uit image bestand")
    print("Optie 7: Elementaire taalherkenning van bestanden uit image bestand")
    print("Optie 8: Indexering van tekst en metadata uit image bestand")
    print("Optie 9: Verwijzing naar duplicaten uit image bestand")
    print("Optie 10: Overzicht van alle afbeeldingen inclusief metadata uit image bestand weergeven")
    print("Optie 11: Overzicht van gebruikersbestanden naat taal uit image bestand")
    print("Optie 12: Herkennen van imageonly PDF en TIFF bestanden uit image bestand")
    print("Optie 13: Sporen van social media weergeven uit image bestand")
    print("Optie 14: Sporen van encryptie weergeven uit image bestand")
    print("Optie 15: Herkenning van VPN uit image bestand weergeven")
    print("Optie 16: Geintalleerde en gebruikte software uit image bestand weergeven")
    print("Optie 17: Analyse van systemfiles uit image bestand maken")
    print("Optie 18: Analyse van VSS/Unpartitioned space uit image bestand maken")
    print("Optie 19: Rapport over ongebruikelijke zaken uit image bestand maken")
    print("Optie 20: Rapport over fragmentatie uit image bestand maken")
    print("Optie 21: Entiteit extractie van geldbedragen uit image bestand maken")
    print("Optie 22: Entiteit extractie van creditcard nummers uit image bestand maken")
    print("Optie 23: Entiteit extractie van telefoonnummers uit image bestand maken")
    print("Optie 24: Entiteit extractie van nummerplaten uit image bestand maken")
    print("Optie 25: Entiteit extractie van bankrekening nummers uit image bestand maken")

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

        extractor(casusNaam, connectie, c, imageBestand, extractsLocatie)

    if(optie == 3):
        print "Het programma wordt over 3 seconden afgesloten..."
        connectie.close()
        time.sleep(3)
        sys.exit()

    if (optie == 4):
        # Requirement 1.1.1 KLAAR
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_extension "
                  "LIKE '.doc' or file_extension like '.ppt' or file_extension like '.xls'")
        # commit
        connectie.commit()
        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie4 = c.fetchall()
        with open('Optie4-compoundExtractie.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie4):
                if i == 0:
                    writer.writerow(['De volgende bestanden zijn geextraheerd en geplaatst in de extracts in de werkmap van de casus:', 'Filetype:'])
                writer.writerow(querie4[i])
                i = i + 1


    if (optie == 5):
        # Requirement 1.1.2
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_extension "
                  "LIKE '.txt' or file_extension like '.doc'")

        #d.execute("select file_name"
         #         "from Files"
          #        "where file_extention"
           #       "LIKE '.txt' or file_extension like '.doc'" )
        # commit
        connectie.commit()
        # maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie5 = c.fetchall()
        with open('Optie5-textUitBestanden.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie5):
                if i == 0:
                    writer.writerow(['Er is van de volgende bestanden tekst geextraheerd:','Filetype:'])
                writer.writerow(querie5[i])
                i = i + 1

    if (optie == 6):
        # Requirement 1.1.3 KLAAR
        c.execute(
            "select file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
            "from Files "
            "where file_extension "
            "LIKE '.pdf' or file_extension like '.doc' or file_extension like '.jpg' or file_extension like '.png'")
        # commit
        connectie.commit()
        # maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie6 = c.fetchall()
        with open('Optie6-metadata.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie6):
                if i == 0:
                    writer.writerow(['Bestandsnaam', 'Extractienaam', 'Bestandstype', 'File aanmaakdatum', 'File modificatiedatum', 'File laatste toegangsdatum'])
                writer.writerow(querie6[i])
                i = i + 1

    if (optie == 7):
        # Requirement 1.1.4
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_extension "
                  "LIKE '.txt' or file_extension like '.doc'")
        # commit
        connectie.commit()
        #Taalherkenning text in Database
    if (optie == 8):
        # Requirement 1.1.5
        c.execute(
            "select file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
            "from Files "
            "where file_extension "
            "LIKE '.txt' or file_extension like '.doc'")
        # commit
        connectie.commit()
        #Na textract in DB


        if (optie == 9):
            # Requirement 1.1.6
            # Tabel tabelDuplicates aanmaken met de volgende kolommen: file_name, file_md5_hash en file_aantal_duplicates
            try:
                sql_command = """CREATE TABLE tabelDuplicates AS
                        SELECT file_name as 'file_name',
                        file_md5_hash as 'file_md5_hash',
                        count(*) as 'file_aantal_duplicates'
                        FROM Files
                        GROUP BY file_md5_hash HAVING count(*) > 1
                        ORDER BY file_name DESC """

                # Voer code uit
                c.execute(sql_command)
                # commit
                connectie.commit()

            except sqlite3.OperationalError as e:
                werkMenu(casusNaam, connectie, c, imageBestand)

    if (optie == 10):
        # Requirement 1.1.7 KLAAR
        c.execute(
            "select file_name, file_extract_name, file_extension, file_md5_hash, file_creation_time, file_modification_time, file_acces_time "
            "from Files "
            "where file_extension "
            "LIKE '.jpg' or file_extension like '.jpeg' or file_extension like '.png' or file_extension like '.tiff'")
        # commit
        connectie.commit()

        querie10 = c.fetchall()
        with open('Optie10-afbeeldingen_meta.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie10):
                if i == 0:
                    writer.writerow(
                        ['Bestandsnaam:', 'Extractienaam:', 'Bestandstype:', 'MD5 hashwaarde:', 'File aanmaakdatum:',
                         'File modificatiedatum:', 'File laatste toegangsdatum:',])
                writer.writerow(querie10[i])
                i = i + 1

    if (optie == 12):
        # Requirement 1.1.9 KLAAR
        c.execute(
            "select file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
            "from Files "
            "where file_extension "
            "LIKE '.pdf' or file_extension like '.tif' or file_extension like '.tiff'")
        # commit
        connectie.commit()

        querie12 = c.fetchall()
        with open('Optie12-imageonly.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie12):
                if i == 0:
                    writer.writerow(
                        ['Bestandsnaam:', 'Extractienaam:', 'Bestandstype:', 'File aanmaakdatum:',
                         'File modificatiedatum:', 'File laatste toegangsdatum:', ])
                writer.writerow(querie12[i])
                i = i + 1

    if (optie == 13):
        # Requirement 1.1.10 KLAAR
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%Bookmark%' or file_name like '%History%' or file_name like '%Facebook%' or file_name like '%Twitter%' or file_name like '%Skype%'")
        # commit
        connectie.commit()

        querie13 = c.fetchall()
        with open('Optie13-socialMedia.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie13):
                if i == 0:
                    writer.writerow(
                        ['Bestandsnaam:', 'Bestandstype:'])
                writer.writerow(querie13[i])
                i = i + 1

    if (optie == 14):
        # Requirement 1.1.11
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%Crypt%' or file_name like '%Lock%' or file_name like '%Safe%'")
        # commit
        connectie.commit()

        querie14 = c.fetchall()
        with open('Optie14-encryptie.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie14):
                if i == 0:
                    writer.writerow(
                        ['Bestandsnaam:', 'Bestandstype:'])
                writer.writerow(querie14[i])
                i = i + 1

    if (optie == 15):
        # Requirement 1.1.12 KLAAR
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%VPN%' or file_name like '%Citrix%'")
        # commit
        connectie.commit()

        querie15 = c.fetchall()
        with open('Optie15-vpn.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie15):
                if i == 0:
                    writer.writerow(
                        ['Bestandsnaam:', 'Bestandstype:'])
                writer.writerow(querie15[i])
                i = i + 1

    if (optie == 19):
        # Requirement 1.1.16 KLAAR
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%Confidential%' or file_name like '%Vertrouwelijk%' or file_name like '%Porn%' or file_name like '%Abuse%' or file_name like '%Misbruik%' or file_name like '%Mishandeling%' or file_name like '%Fraud%'")
        # commit
        connectie.commit()
        querie19 = c.fetchall()
        with open('Optie19-ongebruikelijkeZaken.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            while i < len(querie19):
                if i == 0:
                    writer.writerow(
                        ['Bestandsnaam:', 'Bestandstype:'])
                writer.writerow(querie19[i])
                i = i + 1

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