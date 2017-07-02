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
import csv
#from termcolor import colored


#VARIABELEN
d = datetime.datetime.now()
datum = "%s/%s/%s" %(d.day, d.month, d.year)
tijd = time.strftime("%X")

#Mappen
werkMap = "BMMG_Werkmap"
saveFileMap = "/case_info/"
extractsMap = "/extracts/"
reportsMap = "/reports/"

#SQL Tabelnamen en Kolomnamen
kolomCasusNaam = 'casus_naam'
kolomOnderzoekerNaam = 'onderzoeker_naam'
kolomCasusMap = 'locatie_casusmap'  #locatie casus info map

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

tabelMetaData = 'file_metadata_requirement_1_1_3'
tabelMetaData2 = 'file_metadata_requirement_1_1_7'
tabelPDF_TIFF = 'tabelPDF_TIFF'


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
    casusNaam = raw_input(str("Casus Naam: "))
    casusNaam = "BMMG_Casus_" + casusNaam
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
    #infomap aanmaken in casusmap
    casusInfoMap = casusMap + saveFileMap
    if not os.path.exists(casusInfoMap):
        os.makedirs(casusInfoMap)

    databaseBestandNaam = casusNaam + ".BMMG"

    #databasebestand maken in de savefilemap van de casusmap
    databaseBestand = casusInfoMap + databaseBestandNaam

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
                                             "De savefile is te vinden in de map: "+casusInfoMap+"\n"
                                                                                             "Met behulp van de savefile kunt u verdergaan met de casus wanneer u wilt.\n")
    else:
        print("Welkom " + onderzoekerNaam + "! De casus is aangemaakt.\n"
                                            "De savefile: '" + databaseBestandNaam + "' is aangemaakt.\n"
                                                                           "De savefile is te vinden in de map: "+casusInfoMap+"\n"
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
                                print "-----------------------------------------------------------------------------------------BMMG-Analyzer\n"

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

    #Locatie van de casusmap opvragen uit de database
    c.execute("SELECT {kolomnaam} FROM {tabelnaam}"
              .format(kolomnaam=kolomCasusMap, tabelnaam=casusNaamInfo))
    locatieCMap = c.fetchone()[0]

    #Reportsmap aanmaken
    locatieReports = locatieCMap + reportsMap
    if not os.path.exists(locatieReports):
        os.makedirs(locatieReports)

    locatieExtracts = locatieCMap + extractsMap

    #Werkmenu opties printen op scherm
    print("Optie 1: Casusinformatie opvragen")
    print("Optie 2: Compound Files inzichtelijk maken ")                                                                   #Requirement C.1.1.1
    print("Optie 4: Metadata inzichtelijk maken van bestanden: PDF, DOC, JPG, PNG")                                        #Requirement C.1.1.3
    print("Optie 7: Duplicaten inzichtelijke maken")                                                                       #Requirement C.1.1.6
    print("Optie 8: Metadata inzichtelijk maken van bestanden: JPG, JPEG, PNG, TIFF")                                      #Requirement C.1.1.7
    print("Optie 10: Herkennen van PDF-, en TIFF-bestanden + Metadata extraheren")                                         #Requirement C.1.1.9
    print("Optie 11: Social Media sporen inzichtelijk maken")                                                              #Requirement C.1.1.10
    print("Optie 12: Sporen van encryptie inzichtelijk maken")                                                             #Requirement C.1.1.11
    print("Optie 13: Sporen van VPN/Citrix inzichtelijk maken")                                                            #Requirement C.1.1.12
    print("Optie 14: Software inzichtelijk maken")                                                                         #Requirement C.1.1.13
    print("Optie 15: System Files inzichtelijk maken")                                                                     #Requirement C.1.1.14
    print("Optie 16: FAT-table inzien")                                                                                    #Requirement C.1.1.15
    print("Optie 17: Ongebruikelijke zaken inzichtelijk maken")                                                            #Requirement C.1.1.16
    print("Optie 100: BMMG-Analyzer afsluiten")

    #optie kiezen in het werkmenu
    optie = int(raw_input("\nKies een optie: "))
    if not optie:
        print "Stap 2"
        optie = int(raw_input("\nKies een optie. Vul een optie van hierboven in!!!: "))
        print "Stap 3"
        if not optie:
            optie = int(raw_input("\nKies een optie. Vul een optie van hierboven in!!!: "))
            print ("Twee keer geen optie opgegeven, het programma wordt afgesloten")
            time.sleep(3)
            sys.exit()

###OPTIES#######

    #Casusinformatie opvragen
    if(optie == 1):
        #casusnaam opvragen uit de database en printen op scherm
        c.execute('SELECT * FROM {tabelnaam}'
                  .format(tabelnaam=casusNaamInfo))
        dataUitDB = c.fetchall()
        for value in dataUitDB:
            dataCasusNaam = value[0]
            dataOnderzoeker = value[1]
            dataCasusMap = value[2]
            print"\nCasus Naam: "+ dataCasusNaam
            print "Onderzoeker: " + dataOnderzoeker
            print "Casusmap: " + dataCasusMap + "\n"
            print "U wordt automatisch teruggestuurd naar het werkmenu..."
            time.sleep(5)

        #weer naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.1: Compound files inzichtelijk maken
    if(optie == 2):
        print "BMMG-Analyzer is bezig..."
        #select compound files from database
        c.execute("SELECT file_name, file_extension "
                  "FROM Files "
                  "WHERE file_extension "
                  "LIKE '.doc' OR file_extension LIKE '.ppt' OR file_extension LIKE '.xls'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie4 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "Compound_Files.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie4):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "Compound-file found..."
                writer.writerow(querie4[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met daarin alle Compound-Files"
        print "Dit rapport is te vinden in de map: "+ reportCompound
        print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
        print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.2: Text uit bestanden inzichtelijk maken (TXT + DOC)
    if (optie == 3):
        print ""
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.3: Metadata inzichtelijk maken van bestanden PDF, DOC, JPG, PNG
    if (optie == 4):
        #opslagfile maken voor compound files
        reportMetadata = locatieReports + "Metadata_PDF_DOC_JPG_PNG.csv"#select from database


        try:
            # Metadata tabel maken
            c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=tabelMetaData,
                                                                                 kolomnaam=kolomFileName,
                                                                                 datatype=textDataType))
            # Nieuwe kolommen toevoegen
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData, kolomnaam=kolomFileExtractNameLocation, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData, kolomnaam=kolomFileExtension, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData, kolomnaam=kolomFileCreationTime, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData, kolomnaam=kolomFileModificationTime, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData, kolomnaam=kolomFileAccesTime, datatype=textDataType))
            #commit aanmaken van tabel en kolommen
            connectie.commit()

            #functie voor tijd omzetten van unix naar normal time
            def generateTime(unixTime):
                return (datetime.datetime.fromtimestamp(
                    int(unixTime)
                    # format van de timenotatie
                ).strftime('%Y-%m-%d %H:%M:%S'))

            c.execute(
                "select file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
                "from Files "
                "where file_extension "
                "LIKE '.pdf' or file_extension like '.doc' or file_extension like '.jpg' or file_extension like '.png'")

            UNIXTime = c.fetchall()
            for value in UNIXTime:
                fileName = value[0]
                filePlaats = value[1]
                fileExtensie = value[2]
                try:
                    UNIXreturn1 = generateTime(value[3])
                    UNIXreturn2 = generateTime(value[4])
                    UNIXreturn3 = generateTime(value[5])
                except:
                    print ""

                try:
                    print "--------------NEW FILE-------------------"
                    print "Filename: " + fileName
                    print UNIXreturn1 + " = Creation time"
                    print UNIXreturn2 + " = Modification time"
                    print UNIXreturn3 + " = Acces time\n"

                    #file_metadata tabel vullen
                    c.execute(
                        "INSERT INTO {tabelnaam} ({kolomnaam1},{kolomnaam2},{kolomnaam3},{kolomnaam4},{kolomnaam5},{kolomnaam6})"
                        " VALUES ('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}')"
                            .format(tabelnaam=tabelMetaData, kolomnaam1=kolomFileName, kolomnaam2=kolomFileExtractNameLocation,
                                    kolomnaam3=kolomFileExtension,
                                    kolomnaam4=kolomFileCreationTime, kolomnaam5=kolomFileModificationTime,
                                    kolomnaam6=kolomFileAccesTime,
                                    value1=fileName, value2=filePlaats, value3=fileExtensie, value4=UNIXreturn1,
                                    value5=UNIXreturn2, value6=UNIXreturn3))
                    #commit insert into database
                    connectie.commit()

                except:
                    print ""

            #report maken van gemaakte tabel hierboven
            print "BMMG-Analyzer is bezig..."

            c.execute("SELECT file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
                      "FROM file_metadata_requirement_1_1_3 ")

            #maak een waarde aan die de informatie uit de SQL querie overneemt.
            query = c.fetchall()

            #maak reportfile aan
            with open(reportMetadata, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                i = 0
                #voor elke row uit de select hierboven
                while i < len(query):
                    #Headers aanmaken voor tabel
                    if i == 0:
                        writer.writerow(['File-Name:', 'Locatie:', 'File-Extensie:', 'Creation Time:','Modification Time:', 'Acces Time:'])
                    #anderzijds write hij de data naar de file
                    writer.writerow(query[i])
                    #itereren over de rows uit de database
                    i = i + 1
            print "Er is een rapport gegenereerd met daarin alle Metadata van de bestanden PDF, DOC, JPG, PNG."
            print "Dit rapport is te vinden in de map: "+ reportMetadata
            print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
            print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
            time.sleep(8)

            #terug naar werkmenu
            werkMenu(casusNaam, connectie, c, imageBestand)

        except:
            print "Er is reeds een rapport gegenereerd met daarin alle Metadata van de bestanden PDF, DOC, JPG, PNG."
            print "Dit rapport is te vinden in de map: "+ reportMetadata
            print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
            print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
            time.sleep(8)

            #terug naar werkmenu
            werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.4: Taalherkenning op de bestanden TXT en DOC
    if (optie == 5):
        print ""
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.5: Text en metadata inzichtelijk maken van DOC, TXT
    if (optie == 6):
        print ""
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.6: Duplicaten inzichtelijk maken
    if (optie == 7):
        print ""
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.7: Metadata inzichtelijk maken van bestanden JPG, JPEG, PNG, TIFF
    if (optie == 8):
        #opslagfile maken voor compound files
        reportMetadata2 = locatieReports + "Metadata_JPG_JPEG_PNG_TIFF.csv"#select from database

        try:
            # Metadata tabel maken
            c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=tabelMetaData2,
                                                                                 kolomnaam=kolomFileName,
                                                                                 datatype=textDataType))
            # Nieuwe kolommen toevoegen
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData2, kolomnaam=kolomFileExtractNameLocation, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData2, kolomnaam=kolomFileExtension, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData2, kolomnaam=kolomFileCreationTime, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData2, kolomnaam=kolomFileModificationTime, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelMetaData2, kolomnaam=kolomFileAccesTime, datatype=textDataType))
            #commit aanmaken van tabel en kolommen
            connectie.commit()

            #functie voor tijd omzetten van unix naar normal time
            def generateTime(unixTime):
                return (datetime.datetime.fromtimestamp(
                    int(unixTime)
                    # format van de timenotatie
                ).strftime('%Y-%m-%d %H:%M:%S'))

            c.execute(
                "select file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
                "from Files "
                "where file_extension "
                "LIKE '.jpeg' or file_extension like '.jpg' or file_extension like '.png' or file_extension like '.tiff'")

            UNIXTime = c.fetchall()
            for value in UNIXTime:
                fileName = value[0]
                filePlaats = value[1]
                fileExtensie = value[2]
                try:
                    UNIXreturn1 = generateTime(value[3])
                    UNIXreturn2 = generateTime(value[4])
                    UNIXreturn3 = generateTime(value[5])
                except:
                    print ""

                try:
                    print "--------------NEW FILE-------------------"
                    print "Filename: " + fileName
                    print UNIXreturn1 + " = Creation time"
                    print UNIXreturn2 + " = Modification time"
                    print UNIXreturn3 + " = Acces time\n"

                    #file_metadata tabel vullen
                    c.execute(
                        "INSERT INTO {tabelnaam} ({kolomnaam1},{kolomnaam2},{kolomnaam3},{kolomnaam4},{kolomnaam5},{kolomnaam6})"
                        " VALUES ('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}')"
                            .format(tabelnaam=tabelMetaData2, kolomnaam1=kolomFileName, kolomnaam2=kolomFileExtractNameLocation,
                                    kolomnaam3=kolomFileExtension,
                                    kolomnaam4=kolomFileCreationTime, kolomnaam5=kolomFileModificationTime,
                                    kolomnaam6=kolomFileAccesTime,
                                    value1=fileName, value2=filePlaats, value3=fileExtensie, value4=UNIXreturn1,
                                    value5=UNIXreturn2, value6=UNIXreturn3))
                    #commit insert into database
                    connectie.commit()

                except:
                    print ""

            #report maken van gemaakte tabel hierboven
            print "BMMG-Analyzer is bezig..."

            c.execute("SELECT file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
                      "FROM file_metadata_requirement_1_1_7 ")

            #maak een waarde aan die de informatie uit de SQL querie overneemt.
            query = c.fetchall()

            #maak reportfile aan
            with open(reportMetadata2, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                i = 0
                #voor elke row uit de select hierboven
                while i < len(query):
                    #Headers aanmaken voor tabel
                    if i == 0:
                        writer.writerow(['File-Name:', 'Locatie:', 'File-Extensie:', 'Creation Time:','Modification Time:', 'Acces Time:'])
                    #anderzijds write hij de data naar de file
                    writer.writerow(query[i])
                    #itereren over de rows uit de database
                    i = i + 1
            print "Er is een rapport gegenereerd met daarin alle Metadata van de bestanden PDF, DOC, JPG, PNG."
            print "Dit rapport is te vinden in de map: "+ reportMetadata2
            print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
            print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
            time.sleep(8)

            #terug naar werkmenu
            werkMenu(casusNaam, connectie, c, imageBestand)

        except:
            print "Er is reeds een rapport gegenereerd met daarin alle Metadata van de bestanden PDF, DOC, JPG, PNG."
            print "Dit rapport is te vinden in de map: "+ reportMetadata2
            print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
            print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
            time.sleep(8)

            #terug naar werkmenu
            werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.8: Gebruikers inzichtelijk maken + taalherkenning
    if (optie == 9):
        print ""
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.9: Filename, Metadata + opslaglocatie printen van bestanden PDF, TIFF
    if (optie == 10):

        #opslagfile maken voor compound files
        reportMetadata2 = locatieReports + "Metadata_PDF_TIFF.csv"

        try:
            # Metadata tabel maken
            c.execute('CREATE TABLE {tabelnaam} ({kolomnaam} {datatype})'.format(tabelnaam=tabelPDF_TIFF,
                                                                                 kolomnaam=kolomFileName,
                                                                                 datatype=textDataType))
            # Nieuwe kolommen toevoegen
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelPDF_TIFF, kolomnaam=kolomFileExtractNameLocation, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelPDF_TIFF, kolomnaam=kolomFileExtension, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelPDF_TIFF, kolomnaam=kolomFileCreationTime, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelPDF_TIFF, kolomnaam=kolomFileModificationTime, datatype=textDataType))
            c.execute("ALTER TABLE {tabelnaam} ADD COLUMN '{kolomnaam}' {datatype}"
                      .format(tabelnaam=tabelPDF_TIFF, kolomnaam=kolomFileAccesTime, datatype=textDataType))
            #commit aanmaken van tabel en kolommen
            connectie.commit()

            #functie voor tijd omzetten van unix naar normal time
            def generateTime(unixTime):
                return (datetime.datetime.fromtimestamp(
                    int(unixTime)
                    # format van de timenotatie
                ).strftime('%Y-%m-%d %H:%M:%S'))

            c.execute(
                "select file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
                "from Files "
                "where file_extension "
                "LIKE '.pdf' or file_extension like '.tif' or file_extension like '.tiff'")

            UNIXTime = c.fetchall()
            for value in UNIXTime:
                fileName = value[0]
                filePlaats = value[1]
                fileExtensie = value[2]
                try:
                    UNIXreturn1 = generateTime(value[3])
                    UNIXreturn2 = generateTime(value[4])
                    UNIXreturn3 = generateTime(value[5])
                except:
                    print ""

                try:
                    print "--------------NEW FILE-------------------"
                    print "Filename: " + fileName
                    print UNIXreturn1 + " = Creation time"
                    print UNIXreturn2 + " = Modification time"
                    print UNIXreturn3 + " = Acces time\n"

                    #file_metadata tabel vullen
                    c.execute(
                        "INSERT INTO {tabelnaam} ({kolomnaam1},{kolomnaam2},{kolomnaam3},{kolomnaam4},{kolomnaam5},{kolomnaam6})"
                        " VALUES ('{value1}','{value2}','{value3}','{value4}','{value5}','{value6}')"
                            .format(tabelnaam=tabelPDF_TIFF, kolomnaam1=kolomFileName, kolomnaam2=kolomFileExtractNameLocation,
                                    kolomnaam3=kolomFileExtension,
                                    kolomnaam4=kolomFileCreationTime, kolomnaam5=kolomFileModificationTime,
                                    kolomnaam6=kolomFileAccesTime,
                                    value1=fileName, value2=filePlaats, value3=fileExtensie, value4=UNIXreturn1,
                                    value5=UNIXreturn2, value6=UNIXreturn3))
                    #commit insert into database
                    connectie.commit()

                except:
                    print ""

            #report maken van gemaakte tabel hierboven
            print "BMMG-Analyzer is bezig..."

            c.execute("SELECT file_name, file_extract_name, file_extension, file_creation_time, file_modification_time, file_acces_time "
                      "FROM tabelPDF_TIFF ")

            #maak een waarde aan die de informatie uit de SQL querie overneemt.
            query = c.fetchall()

            #maak reportfile aan
            with open(reportMetadata2, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                i = 0
                #voor elke row uit de select hierboven
                while i < len(query):
                    #Headers aanmaken voor tabel
                    if i == 0:
                        writer.writerow(['File-Name:', 'Locatie:', 'File-Extensie:', 'Creation Time:','Modification Time:', 'Acces Time:'])
                    #anderzijds write hij de data naar de file
                    writer.writerow(query[i])
                    #itereren over de rows uit de database
                    i = i + 1
            print "Er is een rapport gegenereerd met daarin alle Metadata van de bestanden PDF, DOC, JPG, PNG."
            print "Dit rapport is te vinden in de map: "+ reportMetadata2
            print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
            print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
            time.sleep(8)

            #terug naar werkmenu
            werkMenu(casusNaam, connectie, c, imageBestand)

        except:
            print "Er is reeds een rapport gegenereerd met daarin alle Metadata van de bestanden PDF, DOC, JPG, PNG."
            print "Dit rapport is te vinden in de map: "+ reportMetadata2
            print "De bestanden uit dit rapport kunt u terugvinden in de map: " + locatieExtracts
            print "U wordt nu automatisch teruggestuurd naar het werkmenu..."
            time.sleep(8)

            #terug naar werkmenu
            werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.10: Social Media sporen inzichtelijk maken, print filename + locatie
    if (optie == 11):
        #select alle bestanden die sporen van social media bevatten
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%Bookmark%' or file_name like '%History%' or file_name like '%Facebook%' or file_name like '%Twitter%' or file_name like '%Skype%'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie11 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "Social_Media.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie11):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "Social Media found..."
                writer.writerow(querie11[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met een overzicht van bestanden m.b.t. social media."
        print "Dit rapport is te vinden in: "+ reportCompound
        print "De bestanden in dit rapport kunt u terugvinden in: " + locatieExtracts
        print "U wordt automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        werkMenu(casusNaam, connectie, c, imageBestand)

    if (optie == 12):
        #select alle bestanden die sporen van encryptie bevatten
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%Crypt%' or file_name like '%Lock%' or file_name like '%Safe%'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie11 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "Encryption.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie11):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "Encryption found..."
                writer.writerow(querie11[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met een overzicht van bestanden m.b.t. encryptie van data."
        print "Dit rapport is te vinden in: "+ reportCompound
        print "De bestanden in dit rapport kunt u terugvinden in: " + locatieExtracts
        print "U wordt automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        werkMenu(casusNaam, connectie, c, imageBestand)

    if (optie == 13):
        #select alle bestanden die sporen van VPN/Citrix bevatten
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%VPN%' or file_name like '%Citrix%'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie11 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "VPN_Citrix.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie11):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "VPN/Citrix found..."
                writer.writerow(querie11[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met een overzicht van bestanden m.b.t. VPN/Citrix."
        print "Dit rapport is te vinden in: "+ reportCompound
        print "De bestanden in dit rapport kunt u terugvinden in: " + locatieExtracts
        print "U wordt automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        werkMenu(casusNaam, connectie, c, imageBestand)

    if (optie == 14):
        #select alle bestanden die .exe zijn
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_extension "
                  "LIKE '.exe'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie11 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "Applicaties.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie11):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "Applications found..."
                writer.writerow(querie11[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met een overzicht van applicaties die zijn gevonden."
        print "Dit rapport is te vinden in: "+ reportCompound
        print "De bestanden in dit rapport kunt u terugvinden in: " + locatieExtracts
        print "U wordt automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        werkMenu(casusNaam, connectie, c, imageBestand)

    if (optie == 15):
        #select system files
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%hiberfil%' or file_name like '%cookie%' or file_name like '%internet%' or file_name like '%pagefile%' or file_name like '%registry%'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie11 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "System_Files.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie11):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "System files found..."
                writer.writerow(querie11[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met een overzicht van system files."
        print "Dit rapport is te vinden in: "+ reportCompound
        print "De bestanden in dit rapport kunt u terugvinden in: " + locatieExtracts
        print "U wordt automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        werkMenu(casusNaam, connectie, c, imageBestand)

    #Requirement C.1.1.15: Fat-table printen
    if (optie == 16):
        # image handle
        imagehandle = pytsk3.Img_Info(imageBestand)
        # partitie table
        partitionTable = pytsk3.Volume_Info(imagehandle)
        # print partitie tabel
        for partition in partitionTable:
            print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len

        print "U wordt automatisch teruggestuurd naar het werkmenu"
        time.sleep(7)
        #terug naar werkmenu
        werkMenu(casusNaam, connectie, c, imageBestand)

    if (optie == 17):
        #Ongebruikelijke zaken
        c.execute("select file_name, file_extension "
                  "from Files "
                  "where file_name "
                  "LIKE '%Confidential%' or file_name like '%Vertrouwelijk%' or file_name like '%Porn%' or file_name like '%Abuse%' or file_name like '%Misbruik%' or file_name like '%Mishandeling%' or file_name like '%Fraud%'")

        #maak een waarde aan die de informatie uit de SQL querie overneemt.
        querie11 = c.fetchall()
        #opslagfile maken voor compound files
        reportCompound = locatieReports + "Ongebruikelijke_Zaken.csv"

        #maak reportfile aan
        with open(reportCompound, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            i = 0
            #voor elke row uit de select hierboven
            while i < len(querie11):
                #Headers aanmaken voor tabel
                if i == 0:
                    writer.writerow(['File-Name:', 'File-type:'])
                #anderzijds write hij de data naar de file
                print "Bad files found..."
                writer.writerow(querie11[i])
                #itereren over de rows uit de database
                i = i + 1
        print "Er is een rapport gegenereerd met ongebruikelijke zaken."
        print "Dit rapport is te vinden in: "+ reportCompound
        print "De bestanden in dit rapport kunt u terugvinden in: " + locatieExtracts
        print "U wordt automatisch teruggestuurd naar het werkmenu..."
        time.sleep(10)
        werkMenu(casusNaam, connectie, c, imageBestand)

    if(optie == 100):
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