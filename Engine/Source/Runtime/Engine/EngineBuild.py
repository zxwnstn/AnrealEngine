import Anreal

class EngineBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        self.DependencyList.append("Core")
        self.DependencyList.append("Renderer")

    def SetOther(self) :
        self.ModuleName = "Engine"
        self.Executable = True

def GetBuildDesc() :
    return EngineBuildDesc()
