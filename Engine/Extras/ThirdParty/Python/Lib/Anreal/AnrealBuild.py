import os
import sys
import Anreal

RootDir = Anreal.GetAnrealRootDir()
RootOutputDir = RootDir + "/Engine/Binaries/"


def PromptBuildModule(description) :
    print(description.ModuleName)

def BuildOderingByDependencies(buildDescs) : 
    # TODO : Implement Modules ordering by using dependency info 
    pass

def PromptBuildProgram(program) :
    ProgramDir = RootDir + "/Engine/Source/" +  program
    Modules = os.listdir(ProgramDir)

    BuildDescs = []
    for Module in Modules :
        sys.path.append(ProgramDir + '/' + Module)
        BuildScript = __import__(Module + "Build")
        BuildDescs.append(BuildScript.GetBuildDesc())

    BuildOderingByDependencies(BuildDescs)

    for Description in BuildDescs :
        PromptBuildModule(Description)

def RunBuild(args) :
    print("hello build")
    SourceDir = RootDir + '/' + "Engine/Source" 
    ProgramCategories = os.listdir(SourceDir)
    for Program in ProgramCategories :
        PromptBuildProgram(Program)

def RunClean(args) :
    print("hello build")

def RunRebuild(args) :
    RunBuild()
    RunClean()

class BuildCmdList :
    Args = []
    Configs = ""
    IsBuild = False
    IsRebuild = False
    def __init__(self) :
        for cmd in sys.argv :
            if cmd == "-Build" :
                self.IsBuild = True
            elif cmd == "-Rebuild" :
                self.isRebuild = True
            else :
                self.Args.append(cmd)

    def exec(self) :
        if self.IsBuild == True :
            RunBuild(self.Args)
        elif self.IsRebuild == True :
            RunRebuild(self.Args)
        else :
            RunClean(self.Args)

def main() :
    os.chdir(RootDir)
    print("AnrealBuild!")
    CmdList = BuildCmdList()
    CmdList.exec()

if __name__ == '__main__':
    main()
