with open('imagestrings.txt', 'rw') as f:
    file = open("imagestringsnr.txt", "w")
    for line in f:
        y = line.split()
        vari = y[0]
        file.write(vari+"\n")
        print vari

file.close()