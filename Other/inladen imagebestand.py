#python system library
import sys
#forensic image goodness
import pytsk3
#importeren datetime
import datetime
import pyewf
import binascii

# Nodig voor Ewf
class EwfImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EwfImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

#imagebestand
#imagefile = "/media/sf_D_DRIVE/Windows10.E01"
imagefile = "/media/sf_fict/image.dd"

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
                    print "MAP GEVONDEN !!!111"
                    checkDirectory(file.as_directory())
                
                # Bestand gevonden, doe er iets mee
                else:
                    header_bytes = file.read_random(0, 16)
                    print binascii.hexlify(header_bytes)
                    # als de hex bytes overeenkomen met wat je zoekt
                    # exporteer bestand
                    if 'match' == 'matcssh':
                        fh = open("mapje/bestandsnaam.extensie", 'w')
                        fh.write(file.read_random(0, f.info.meta.size))
                        fh.close()

                    print file.info.name.name
            except:
                print "boem"


#partitie table
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