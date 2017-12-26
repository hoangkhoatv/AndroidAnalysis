from __future__ import print_function

import re
import pdb
def readFile():
    file1 = open("CatSources.txt","r") 
    file3 = open("CatSinks.txt","r") 
    cutSources = []
    fullSources = []
    for line in file1:
        check = line.rfind('( ')
        if check !=-1:
            first = line.rfind('<')
            last = line.rfind(':')
            if(first!=-1):
                regex = re.compile(r"(\> )+.+\)")
                sCat = re.search(regex, line).group()
                sCat = sCat[3:len(sCat)-1]
                index = sCat.rfind('(')
                if (index != -1):
                    sCat = sCat[index+1:]
                #keys:getDeviceID, value: library, catalog
                tmp = {"keys" : line[0:check+1], "value" : line[first+1:last],"catalog":sCat}
                cutSources.append(tmp)
            fullSources.append(line)
    cutSinks = []
    fullSinks = []
    for line in file3:
        check = line.rfind('( ')
        if check !=-1:
            first = line.rfind('<')
            last = line.rfind(':')
            if(first!=-1):
                index = line.rfind(line[0:check+1])
                outdex = line.rfind(')>')
                if index!=-1:
                    strInput = line[index+ len(line[0:check+1]):outdex]
                    regex = re.compile(r" (\()+.+(\))")
                    sCat = re.search(regex, line).group()
                    sCat = sCat[2:len(sCat)-1]
                    index = sCat.rfind('(')
                    if (index != -1):
                        sCat = sCat[index:]
                    #keys:getDeviceID, value: library, catalog
                    tmp = {"keys" : line[0:check+1], "value" : line[first+1:last],"input":strInput.split(','),"catalog":sCat}
                    cutSinks.append(tmp)
            fullSinks.append(line)
    # reutrn list source sink
    return cutSources, cutSinks

def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string)
    return string
def getReplace():
    listImport = []
    listReplace = []
    file2 = open("KQ1.txt",'r')
    full = file2.read()
    file2.close()
    file2 = open("KQ1.txt",'r')
    strPackage = file2.readline().rstrip()
    strRpackage = strPackage.replace("package ","").replace(";","")
    #Lay thu vien tu import
    for line in file2:
        check = line.rstrip().rfind('import ')
        if check !=-1:
            strTmp = line[check+7:]
            listReplace.append(strTmp.replace(";", ""))
            strImport =  strTmp.split('.')
            strSearch = strImport[len(strImport)-1]
            listImport.append(strSearch.replace(";", ""))
    return listReplace,strRpackage,listImport,full

def optimizeList(listReplace,package,listImport,listFull):
    #thay the ten class bang package
    listFull = removeComments(listFull)
    index = listFull.rfind("public class ")
    strClass = "public class "
    regex = re.compile(r"public class +[a-zA-Z1-9_]+.")
    if( index == -1):
        index = listFull.rfind("public final class ")
        strClass = "public final class "
        regex = re.compile(r"public final class +[a-zA-Z1-9_]+.")
    listFull= listFull[index:] 
    sClass = re.search(regex, listFull)
    sClass = sClass.group()
    sInsert = sClass.replace(strClass,"")
    strFull = listFull.replace(sClass,strClass+package+"."+sInsert)
    for x in range(0,len(listImport)):
        listImport[x] = listImport[x].replace('\r\n','')
    for x in range(0,len(listReplace)):
        listReplace[x] = listReplace[x].replace('\r\n','')
    i = 0
    #Thay the cac khai bao bien thanh ten thu vien
    for x in listImport:       
        strFull = strFull.replace(" "+x.rstrip('\n') + " ", listReplace[i].rstrip('\n') + " ")
        strFull = strFull.replace("(" + x.rstrip('\n') + ".", "(" + listReplace[i].rstrip('\n') +  ".")
        strFull = strFull.replace(" " + x.rstrip('\n') + "(", " " + listReplace[i].rstrip('\n') +  "(")
        strFull = strFull.replace(" " + x.rstrip('\n') + ".", " " + listReplace[i].rstrip('\n') +  ".")
        strFull = strFull.replace("," + x.rstrip('\n') + ".", "("+listReplace[i].rstrip('\n') +  ".")
        strFull = strFull.replace("(" + x.rstrip('\n') + ")", "("+listReplace[i].rstrip('\n') +  ")")
        i = i + 1
    # tach list string moi ; la mot hang
    listCham =  strFull.split(';')
    listFCham = []
    tmp =package+"."+sInsert.strip()
    listImport.append(tmp)
    #xoa cac if elese while va dau lien quan {}
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
    listIF = []
    for x in listBang:
        x = x.replace("if ","")
        x = x.replace("else ","")
        x = x.replace("while ","")
        x = x.replace("return ","")
        x = x.replace("try ","")
        x = x.replace("catch ","")
        listIF.append(x.strip())
    return listIF

def getSourceSink(listOp,cutSources,cutSinks,listImport,listReplace):
    listCheck = []
    listCheckSink = []
    i = len(listOp)-1
    #tim soucre trong mang tu tren xuong
    while (i >=0):
        isSource = 0
        listKeys = []
        fSource = ""
        for y in cutSources:
            if listOp[i].rfind(y['keys']) != -1:
                value1 = y['value']
                k = i-1
                while (k>=0):
                    if listOp[k].rfind(value1+" ")!=-1:
                        isSource=1
                        if listOp[i-1].rfind(" =")!=-1:
                            if not listOp[i-1] + listOp[i] in listKeys:
                                listKeys.insert(0,listOp[i-1] + listOp[i])
                            regex = re.compile(r".[a-zA-Z1-9]+( =)")
                            fSource = re.search(regex, listOp[i-1]).group().strip().replace(" =","")
                        else:
                            if not listOp[i] in listKeys:
                                listKeys.insert(0,listOp[i])
                        if listOp[k].rfind(" =")!=-1:
                            if not listOp[k]+ listOp[k+1] in listKeys:
                                listKeys.insert(0,listOp[k] + listOp[k+1])
                        else:
                            if not listOp[k] in listKeys:
                                listKeys.insert(0,listOp[k])
                        regex = re.compile(r"=+[a-zA-Z1-9_]+.")
                        sSource = re.search(regex, listOp[i-1] + listOp[i])
                        if(sSource != None):
                            value2 = sSource.group()
                            value2 = value2[1:len(value2)]
                            for z in range(i-2,k,-1):
                                if listOp[z].rfind(value2) != -1:
                                    if not listOp[z] in listKeys:
                                        listKeys.insert(1,listOp[z])
                    k = k -1
            if listKeys != []:
                listCheck.append({"keys": listKeys,"value":y,"source":fSource})
                break
            if isSource == 1:
                break
        i = i -1
    i =  len(listOp)-1
    last = []
    #tim sink trong mang tu duoi len
    while i >= 0:
        isSink = 0
        listKeys = []
        sSink = ""
        for y in cutSinks:
            if listOp[i].rfind(y['keys'])!=-1:
                regex = re.compile(r"(\()+.+[a-zA-Z1-9]+(\))")
                sInput = re.search(regex, listOp[i])
                if sInput != None:
                    strInput = sInput.group()
                    if (strInput[0] == "(" ):
                        listInput = strInput[1:len(strInput)-1]
                        listInput = listInput.split(',')
                else:
                    strInput = []
                    listInput = []
                for x in listReplace:
                    if x.rstrip('\n') == y['value']:
                        if len(y['input']) == len(listInput):
                            for z in listInput:
                                k = i-1
                                while (k>=0):
                                    if k not in last:
                                        if listOp[k].rfind(z + " ") !=- 1:
                                            if not listOp[i] in listKeys:
                                                last.append(i)
                                                listKeys.insert(0,listOp[i])
                                            if listOp[k].rfind(z+".") != -1:
                                                if not listOp[k] in listKeys:
                                                    last.append(k)
                                                    last.append(k+1)
                                                    listKeys.insert(0,listOp[k])
                                            isSink =1
                                            regex = re.compile(r" +[a-zA-Z1-9_]+ =")
                                            sSink = re.search(regex, listOp[k]).group()
                                            sSink = sSink.replace(" =","").strip()
                                            for h in range (k+1,i):
                                                if listOp[h].rfind(sSink+".") !=-1:
                                                    if not listOp[h] in listKeys:
                                                        last.append(h)
                                                        listKeys.insert(0,listOp[h])
                                    k = k -1
                                if isSink ==1:
                                    break
                    if isSink ==1:
                                    break                                                      
            if listKeys != []:
                listCheckSink.append({"keys": listKeys,"value":y,"sink":sSink})
                break
        i = i- 1
    return listCheck,listCheckSink

def getFlow(listCheck,listCheckSink):
    if listCheckSink == []:
        print ('No Flow')
    else:
        check = 0
        for sink in listCheckSink:
            for source in listCheck:
                    strSource = source['source']
                    if(source['source'] == sink['sink']):
                        for key in sink['keys']:
                                if key.rfind(strSource) != -1:
                                    print ('\n///Have Flow///')
                                    print ("SOURCE: "+source['value']['catalog'])
                                    for x in source['keys']:
                                         print('|'+x+'~source')
                                    print ("SINK: "+sink['value']['catalog'])
                                    for x in sink['keys']:
                                        print('|'+x+'~sink')
                                    check =1
                                    break
        if check == 0:
            print ('No Flow')
       
def main():
    cutSources,cutSinks = readFile()
    listReplace,package,listImport,listFull = getReplace()
    listOp = optimizeList(listReplace,package,listImport,listFull)
    listCheck,listCheckSink = getSourceSink(listOp,cutSources,cutSinks,listImport,listReplace)
    getFlow(listCheck,listCheckSink)

if __name__ == '__main__':
    main()