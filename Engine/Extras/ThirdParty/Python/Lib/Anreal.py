import os

def GetAnrealRootDir() :
    Ret = os.getcwd()
    StrList = Ret.split('\\')
    Rootindex = len(StrList) - 4
    Index = 0
    RootPath = ""
    
    for i in StrList:
        if Index == Rootindex:
            break
        Slash = "/"
        if Index == Rootindex- 1:
            Slash = ""
        RootPath += i + Slash
        Index = Index + 1

    Ret = RootPath
    return Ret

class BuildDesc :
    ModuleName = ""
    DependencyList = {}
    def __init__(self) :
        self.SetDependency()
        self.SetOther()
    
    def SetDependency(self) :
        pass
    
    def SetOther(self) :
        pass
    