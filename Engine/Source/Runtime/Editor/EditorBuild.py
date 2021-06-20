import Anreal

class EditorBuildDesc(Anreal.BuildDesc) :
    def SetDependency(self) :
        print("EditorBuild SetDependency")

    def SetOther(self) :
        self.ModuleName = "Editor"

def GetBuildDesc() :
    return EditorBuildDesc()
