import os

def GetAnrealRootDir() :
    Ret = os.getcwd()
    print("GetAnrealRootDir****" + Ret)
    strList = Ret.split('\\')
    Rootindex = len(strList) - 4
    index = 0
    rootPath = ""
    
    for i in strList:
        if index == Rootindex:
            break
        slash = "/"
        if index == Rootindex- 1:
            slash = ""
        rootPath += i + slash
        index = index + 1

    Ret = rootPath
    print(Ret)
    return Ret