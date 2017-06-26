#python system library
import sys
#forensic image goodness
import pytsk3
#importeren datetime
import datetime


#imagebestand
imagefile = "/media/sf_sf/Windows10.E01"

#image handle
imagehandle = pytsk3.Img_Info(imagefile)

#partitie table
partitionTable = pytsk3.Volume_Info(imagehandle)

#print partitie tabel
for partition in partitionTable:
    print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len

filesystemObject = pytsk3.FS_Info(imagehandle, offset=1048576)

fileobject = filesystemObject.open("/Recovery/WindowsRE/boot.sdi")
print "\nFile Inode:",fileobject.info.meta.addr
print "File Name:",fileobject.info.name.name
print "File Creation Time:",datetime.datetime.fromtimestamp(fileobject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')+"\n"

outfile = open('DFIRWizard-ouput', 'w')
filedata = fileobject.read_random(0,fileobject.info.meta.size)
outfile.write(filedata)

path = "/Boot" #verander naar / voor root directory
inode = 160 #verander naar 0 voor root directory

directory = filesystemObject.open_dir(path=path, inode=inode)

print 'Directories:'

for f in directory:
    print f.info.meta.size, f.info.name.name

outfile2 = open ('boot.sdi','w')
fd = fileobject.read_random(0,fileobject.info.meta.size)
outfile2.write(fd)

f = filesystemObject.open_meta(inode = 174)

print '\n'

print f.info.meta.type
