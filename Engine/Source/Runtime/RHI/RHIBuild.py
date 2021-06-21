import Anreal

class RHIBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        self.DependencyList.append("Core")

    def SetOther(self) :
        self.ModuleName = "RHI"

def GetBuildDesc() :
    return RHIBuildDesc()
