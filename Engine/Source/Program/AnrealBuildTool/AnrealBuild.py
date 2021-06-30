import os
import sys
import Anreal

RootDir = Anreal.GetAnrealRootDir()
RootOutputDir = RootDir + "/Engine/Binaries/"

def ParseAndGetClCmdLine(config, includePath, description) :
    return ""

def ParseAndGetLinkCmdLine(config, libPath, description) :
    return ""

def PromptBuildModule(args, description) :
    print("Module : {0}".format(description.ModuleName))
    CLCommandLine = ParseAndGetClCmdLine(args["Config"], args["IncludePaths"], description)
    #os.system(CLCommandLine)

    LinkCommandLine = ParseAndGetLinkCmdLine(args["Config"], args["LibPaths"], description)
    #os.system(LinkCommandLine)

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
        if Program == "Program" : 
            continue
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

        MergedCmd = ""
        FirstSplitedCmd = []
        for cmd in sys.argv :
            MergedCmd += cmd
        FirstSplitedCmd = MergedCmd.split('-')

        # naive cmd legend (indicate FirstSplitedCmd)
        # 0 - Exec argument
        # 1 - BuildType
        # 2 - Config
        # 3, 4 - Basic Include path
        # 5, 6 - Basic Lib path 

        # First - Set build type and erase elm unnecessaries
        BuildType = FirstSplitedCmd[1]
        if BuildType == "Build" :
            self.IsBuild = True
        elif BuildType == "ReBuild" :
            self.IsRebuild = True
        # Second - Set Config flag
        self.Args["Config"] = FirstSplitedCmd[2]

        # Third - Fill include path with exactly tokkenized paths FirstSplitedCmd[3], FirstSplitedCmd[4]
        IncludePathList = []
        FullIncludePath = FirstSplitedCmd[3] + FirstSplitedCmd[4]
        TokkenizedIncludePaths = FullIncludePath.split(';')
        for path in TokkenizedIncludePaths :
            path.strip()
            if path != "" :
                IncludePathList.append(path)
                # print(path)
        self.Args["IncludePaths"] = IncludePathList

        # Forth - Fill lib path with exactly tokkenized paths FirstSplitedCmd[5], FirstSplitedCmd[6]
        LibPathList = []
        FullLibPath = FirstSplitedCmd[5] + FirstSplitedCmd[6]
        TokkenizedIncludePaths = FullLibPath.split(';')
        for path in TokkenizedIncludePaths :
            path.strip()
            if path != "" :
                LibPathList.append(path)
                # print(path)
        self.Args["LibPaths"] = LibPathList

    def exec(self) :
        if self.IsBuild == True :
            RunBuild(self.Args)
        elif self.IsRebuild == True :
            RunRebuild(self.Args)
        else :
            RunClean()

def main() :
    os.chdir(RootDir)
    print("AnrealBuildTool")
    CmdList = BuildCmdList()
    CmdList.exec()

if __name__ == '__main__':
    main()
