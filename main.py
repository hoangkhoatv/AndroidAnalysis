import re
file1 = open("CatSources.txt","r") 
sources = []
for line in file1:
    check = line.rfind('( <')
    # if check !=-1:
    #     print line[0:check]
    sources.append(line)
def getReplace():
    listImport = []
    listReplace = []
    file2 = open("Activity.java",'r')
    full = file2.read()
    file2.close()
    file2 = open("Activity.java",'r')
    strPackage = file2.readline().rstrip()
    strRpackage = strPackage.replace("package ","").replace(";","")
    for line in file2:
        check = line.rstrip().rfind('import ')
        if check !=-1:
            strTmp = line[check+7:]
            listReplace.append(strTmp.replace(";", ""))
            strImport =  strTmp.split('.')
            strSearch = strImport[len(strImport)-1]
            listImport.append(strSearch.replace(";", ""))
    return listReplace,strRpackage,listImport,full

listReplace,package,listImport,listFull = getReplace()
index = listFull.rfind("public class Activity")
listFull =  listFull[index:]
strFull = listFull.replace("public class Activity","public class "+package+".Activity")
i = 0
for x in listImport:
    strFull = strFull.replace(x.rstrip('\n') + " ", listReplace[i].rstrip('\n') + " ")
    strFull = strFull.replace("(" + x.rstrip('\n') + ".", "(" + listReplace[i].rstrip('\n') +  ".")
    strFull = strFull.replace(","+x.rstrip('\n') + ".", "("+listReplace[i].rstrip('\n') +  ".")
    i = i + 1
listCham =  strFull.split(';')
listFCham = []
for x in listCham:
    tmp = x.replace("\n","")
    tmp = ' '.join(tmp.split())
    listFCham.append(tmp)
listNgoac = []
for x in listFCham:
    tmp = x.split('{')
    for y in tmp:
        listNgoac.append(y)
listFNgoac = []
for x in listNgoac:
    tmp = x.replace("}","")
    listFNgoac.append(tmp)
listBang = []
for x in listFNgoac:
    index = x.rfind(' = ')
    if index !=-1:
        listBang.append(x[:index+3])
        listBang.append(x[index+3:])
    else:
        listBang.append(x)
print listBang


