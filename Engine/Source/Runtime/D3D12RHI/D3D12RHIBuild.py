import Anreal

class D3D12RHIBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        print("D3D12RHIBuild SetDependency")

    def SetOther(self) :
        self.ModuleName = "D3D12RHI"

def GetBuildDesc() :
    return D3D12RHIBuildDesc()
