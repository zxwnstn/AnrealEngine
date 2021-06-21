import Anreal

class EngineBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        self.DependencyList.append("Core")
        self.DependencyList.append("Renderer")

    def SetOther(self) :
        self.ModuleName = "Engine"

def GetBuildDesc() :
    return EngineBuildDesc()
