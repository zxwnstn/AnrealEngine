import Anreal

class RendererBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        print("RendererBuild SetDependency")

    def SetOther(self) :
        self.ModuleName = "Renderer"

def GetBuildDesc() :
    return RendererBuildDesc()
