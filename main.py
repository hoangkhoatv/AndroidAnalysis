file1 = open("CatSources.txt","r") 
sources = []
for line in file1:
    check = line.rfind('( <')
    # if check !=-1:
    #     print line[0:check]
    sources.append(line)
file2 = open("Activity.java",'r')
for line in file2:
    check = line.rfind('import ')
    if check !=-1:
        print line