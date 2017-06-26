import sh

image = "/Windows10.E01"

file = open("strings.txt","w")

stringss = str(sh.strings("-td",image))

file.write(stringss)
file.close()