import Anreal

class D3D12RHIBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        self.DependencyList.append("Core")
        self.DependencyList.append("RHI")

    def SetOther(self) :
        self.ModuleName = "D3D12RHI"

def GetBuildDesc() :
    return D3D12RHIBuildDesc()
