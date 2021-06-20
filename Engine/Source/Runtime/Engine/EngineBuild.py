import Anreal

class EngineBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        print("EngineBuild SetDependency")

    def SetOther(self) :
        self.ModuleName = "Engine"

def GetBuildDesc() :
    return EngineBuildDesc()
