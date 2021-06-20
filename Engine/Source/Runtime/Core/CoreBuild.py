import Anreal

class CoreBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        print("CoreBuild SetDependency")

    def SetOther(self) :
        self.ModuleName = "Core"

def GetBuildDesc() :
    return CoreBuildDesc()
