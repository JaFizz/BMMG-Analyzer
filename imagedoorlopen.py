# python system library
#import sys
#import os
# forensic image goodness
import pytsk3
# importeren datetime
#import datetime
import pyewf
import binascii


# Nodig voor Ewf
class EwfImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EwfImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)


# imagebestand
imagefile = "/media/sf_IPFIT5_Image/Windows10.E01"
#imagefile = "/media/sf_fict/image.dd"

imagetype = "raw"

# E01:
if imagetype == "e01":
    imagefilename = pyewf.glob(imagefile)
    handle = pyewf.handle()
    handle.open(imagefilename)
    image = EwfImgInfo(handle)

# DD
elif imagetype == "raw":
    image = pytsk3.Img_Info(imagefile)


# Loop door een mapje
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
partitionTable = pytsk3.Volume_Info(image)
bsize = partitionTable.info.block_size

for part in partitionTable:
    print part
    try:
        partitionHandle = pytsk3.FS_Info(image, offset=(part.start * bsize))
        directoryHandle = partitionHandle.open_dir(path='/')
        checkDirectory(directoryHandle)
    except IOError as error:
        print ""