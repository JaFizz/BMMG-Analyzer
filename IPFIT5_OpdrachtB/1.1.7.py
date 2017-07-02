import sys
import pytsk3
import datetime
imagefile = "Windows10.E01"
imagehandle = pytsk3.Img_Info(imagefile)
partitionTable = pytsk3.Volume_Info(imagehandle)
for partition in partitionTable:
  print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
filesystemObject = pytsk3.FS_Info(imagehandle, offset=1048576)
fileobject = filesystemObject.open("/$MFT")
print "File Inode:",fileobject.info.meta.addr
print "File Name:",fileobject.info.name.name
print "File Creation Time:",datetime.datetime.fromtimestamp(fileobject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
outfile = open('DFIRWizard-output', 'w')
filedata = fileobject.read_random(0,fileobject.info.meta.size)
outfile.write(filedata)

pytsk3 en pyewf heeft een optie om elke file langs te gaan.
die optie kan je bij elke file die je tegenkomt kijken of je die wel of niet wil
je begint in root met het pad
je except. en ..
dan sub directories
kijken