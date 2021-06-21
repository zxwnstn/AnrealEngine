import os
import sys
import Anreal

RootDir = Anreal.GetAnrealRootDir()
RootOutputDir = RootDir + "/Engine/Binaries/"
CLDir = "C:/\"Program Files (x86)\"/\"Microsoft Visual Studio\"/2019/Community/VC/Tools/MSVC/14.28.29910/bin/Hostx64/x64"

def PromptBuildModule(args, description) :
    print("Module : {0}".format(description.ModuleName))
    CLCommandLine = CLDir + "/cl.exe"
    os.system(CLCommandLine)

def FindAsName(moduleName, buildDesc) :
    for Description in buildDesc :
        if Description.ModuleName == moduleName :
            return Description

def BuildOderingByDependencies(buildDescs) : 
    WorkList = buildDescs
    OrdererdBuildDescList = []

    while len(WorkList) != 0 :
        for Description in WorkList :
            if len(Description.DependencyList) == 0 :
                CheckedModule = Description.ModuleName
                OrdererdBuildDescList.append(FindAsName(CheckedModule, buildDescs))
                WorkList.remove(Description)
                for Description in WorkList :
                    for Dependency in Description.DependencyList :
                        if Dependency == CheckedModule :
                            Description.DependencyList.remove(CheckedModule)
                            break

    return OrdererdBuildDescList

def PromptBuildProgram(args, program) :
    print("Start Build Program : {0}".format(program))
    ProgramDir = RootDir + "/Engine/Source/" +  program
    Modules = os.listdir(ProgramDir)

    BuildDescList = []
    for Module in Modules :
        sys.path.append(ProgramDir + '/' + Module)
        BuildScript = __import__(Module + "Build")
        Description = BuildScript.GetBuildDesc()
        BuildDescList.append(Description)

    OrdererdBuildDescList = BuildOderingByDependencies(BuildDescList)

    for Description in OrdererdBuildDescList :
        PromptBuildModule(args, Description)

def RunBuild(args) :
    SourceDir = RootDir + '/' + "Engine/Source" 
    ProgramCategories = os.listdir(SourceDir)
    for Program in ProgramCategories :
        PromptBuildProgram(args, Program)

def RunClean() :
    print("hello Clean")

def RunRebuild(args) :
    RunClean()
    RunBuild(args)

class BuildCmdList :
    def __init__(self) :
        self.Args = {}
        self.IsBuild = False
        self.IsRebuild = False
        i = 0
        for cmd in sys.argv :
            if i == 1 :
                if cmd == "-Build" :
                    self.IsBuild = True
                elif cmd == "-Rebuild" :
                    self.isRebuild = True
            if i == 2 :
                self.Args["Configs"] = cmd
            i += 1

    def exec(self) :
        if self.IsBuild == True :
            RunBuild(self.Args)
        elif self.IsRebuild == True :
            RunRebuild(self.Args)
        else :
            RunClean()

def main() :
    os.chdir(RootDir)
    print("AnrealBuild!")
    CmdList = BuildCmdList()
    CmdList.exec()

if __name__ == '__main__':
    main()
