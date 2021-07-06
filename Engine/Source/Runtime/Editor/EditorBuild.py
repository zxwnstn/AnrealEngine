import Anreal

class EditorBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        self.DependencyList.append("Core")
        self.DependencyList.append("Renderer")

    def SetOther(self) :
        self.ModuleName = "Editor"

def GetBuildDesc() :
    return EditorBuildDesc()
