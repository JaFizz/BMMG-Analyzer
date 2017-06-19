#python system library
import sys
#forensic image goodness
import pytsk3
#importeren datetime
import datetime


#imagebestand
imagefile = "Windows10.E01"

#image handle
imagehandle = pytsk3.Img_Info(imagefile)

#partitie table
partitionTable = pytsk3.Volume_Info(imagehandle)

#print partitie tabel
for partition in partitionTable:
    print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len

filesystemObject = pytsk3.FS_Info(imagehandle, offset=1048576)

fileobject = filesystemObject.open("/$MFT")
print "\nFile Inode:",fileobject.info.meta.addr
print "File Name:",fileobject.info.name.name
print "File Creation Time:",datetime.datetime.fromtimestamp(fileobject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')

outfile = open('DFIRWizard-ouput', 'w')
filedata = fileobject.read_random(0,fileobject.info.meta.size)
outfile.write(filedata)