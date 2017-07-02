import sh


image = "Windows10.E01"
hallo = "hallo.txt"

file = open("imagestrings.txt","w")

stringss = str(sh.strings("-td",hallo,))



print stringss

file.write(stringss)
file.close()
