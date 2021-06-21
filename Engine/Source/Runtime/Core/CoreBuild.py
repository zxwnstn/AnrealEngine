import Anreal

class CoreBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        pass

    def SetOther(self) :
        self.ModuleName = "Core"

def GetBuildDesc() :
    return CoreBuildDesc()
