import Anreal

class RendererBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        self.DependencyList.append("Core")
        self.DependencyList.append("RHI")

    def SetOther(self) :
        self.ModuleName = "Renderer"

def GetBuildDesc() :
    return RendererBuildDesc()
