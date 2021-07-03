import os
import sys
import Anreal
import json

def ParseAndGetClCmdLine(args, clOptions, description) :
    ClCmdLine = ""

    #formating execute Cl command
    ClPath =  args["VCRuntime"]
    Index = ClPath.find('\\')
    ClPath = ClPath[:Index] + '\"' + ClPath[Index:]

    #Execute cl.exe command
    ClCmdLine += ClPath + "\"" + "\cl.exe"

    #Add Basic Include Paths
    IncludePaths = args["IncludePaths"]
    for includePath in IncludePaths:
        ClCmdLine += " /I \"" + includePath + "\""

    #Add Module Include Path
    ClCmdLine += " /I \"" + description.ProgramPath + "\""
    ClCmdLine += " /I \"" + description.ModulePath + "\"" 
    ClCmdLine += " /I \"" + description.ModulePath + "/public\"" 

    #Gather and attach cpp files that will be compile
    CppFiles = []
    Anreal.GatherFilesFromRecursiveIterate(CppFiles, description.ModulePath, "cpp")
    for Cpp in CppFiles :
        ClCmdLine += ' ' + Cpp

    #Attach native build options
    for clOpt in clOptions :
        ClCmdLine += ' ' + clOpt

    return ClCmdLine

def ParseAndGetLinkCmdLine(args, buildConfigOptions, description) :
    return ""

def PromptBuildModule(args, buildConfigOptions, description) :
    os.chdir(Anreal.ObjPath)
    CLCommandLine = ParseAndGetClCmdLine(args, buildConfigOptions["CL"], description)
    os.system(CLCommandLine)

    os.chdir(Anreal.BinPath)
    LinkCommandLine = ParseAndGetLinkCmdLine(args, buildConfigOptions["Link"], description)
    #os.system(LinkCommandLine)

def FindBuildDescAsName(moduleName, buildDesc) :
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
                OrdererdBuildDescList.append(FindBuildDescAsName(CheckedModule, buildDescs))
                WorkList.remove(Description)
                for Description in WorkList :
                    for Dependency in Description.DependencyList :
                        if Dependency == CheckedModule :
                            Description.DependencyList.remove(CheckedModule)
                            break

    return OrdererdBuildDescList

def GetNativeConfigOpt(abstractedConfigs, complier) :
    
    with open(Anreal.ConfigPath + "/Build/Platform/MSVC.json") as MSVCConfigJson :
        MSVCConfigs = json.load(MSVCConfigJson)

    ConfigList = MSVCConfigs[complier]
    NativeConfigList = {}
    NativeConfigList["CL"] = []
    NativeConfigList["Link"] = []

    for AbstractedConfig in abstractedConfigs :
        if AbstractedConfig in ConfigList["CL"] :
            NativeConfigList["CL"].append(ConfigList["CL"][AbstractedConfig])
        elif AbstractedConfig in ConfigList["Link"] :
            NativeConfigList["Link"].append(ConfigList["Link"][AbstractedConfig])

    return NativeConfigList

def ParseAndGetBuildConfigOptions(args) :
    with open(Anreal.ConfigPath + "/Build/EngineConfig.json") as EngineConfigJson :
        EngineConfigs = json.load(EngineConfigJson)

    CommonConfigs = EngineConfigs["Common"]
    AbstractedConfigs = EngineConfigs[args["Config"]]
    for CommonConfig in CommonConfigs :
        AbstractedConfigs.append(CommonConfig)

    return GetNativeConfigOpt(AbstractedConfigs, args["Compiler"])

def PromptBuildProgram(args, program) :
    ProgramPath = Anreal.RootPath + "/Engine/Source/" +  program
    Modules = os.listdir(ProgramPath)

    BuildConfigOptions = ParseAndGetBuildConfigOptions(args)

    BuildDescList = []
    for Module in Modules :
        if Module == "PublicPCH" :
            continue

        ModulePath = ProgramPath + '/' + Module
        sys.path.append(ModulePath)
        BuildScript = __import__(Module + "Build")
        Description = BuildScript.GetBuildDesc()
        Description.ProgramPath = ProgramPath
        Description.ModulePath = ModulePath
        BuildDescList.append(Description)

    OrdererdBuildDescList = BuildOderingByDependencies(BuildDescList)
    for Description in OrdererdBuildDescList :
        PromptBuildModule(args, BuildConfigOptions, Description)

def RunBuild(args) :
    SourceDir = Anreal.RootPath + '/' + "Engine/Source" 
    ProgramCategories = os.listdir(SourceDir)
    for Program in ProgramCategories :
        if Program == "Program" : 
            continue
        PromptBuildProgram(args, Program)

def RunClean() :
    pass 

def RunRebuild(args) :
    RunClean()
    RunBuild(args)

class MSCVBuildCmdList(Anreal.BuildCmdList) :
    def __init__(self, FirstSplitedCmd) :
        # MSVC cmd legend (indicate FirstSplitedCmd)
        # 0 - Exec argument
        # 1 - BuildType
        # 2 - Config
        # 3, 4 - Basic Include path
        # 5, 6 - Basic Lib path 
        Anreal.BuildCmdList.__init__(self)

        # First - Set build type and erase elm unnecessaries
        BuildType = FirstSplitedCmd[1].strip()
        if BuildType == "Build" :
            self.IsBuild = True
            print("build")
        elif BuildType == "ReBuild" :
            self.IsRebuild = True

        # Second - Set Config flag
        self.Args["Compiler"] = FirstSplitedCmd[2].strip()
        self.Args["Config"] = FirstSplitedCmd[3].strip()

        # Third - Fill include path with exactly tokkenized paths FirstSplitedCmd[4], FirstSplitedCmd[5]
        IncludePathList = []
        FullIncludePath = FirstSplitedCmd[4] + FirstSplitedCmd[5]
        TokkenizedIncludePaths = FullIncludePath.split(';')
        for path in TokkenizedIncludePaths :
            path.strip()
            if path != "" :
                IncludePathList.append(path)
        self.Args["IncludePaths"] = IncludePathList

        # Forth - Fill lib path with exactly tokkenized paths FirstSplitedCmd[6], FirstSplitedCmd[7]
        LibPathList = []
        FullLibPath = FirstSplitedCmd[5] + FirstSplitedCmd[6]
        TokkenizedIncludePaths = FullLibPath.split(';')
        for path in TokkenizedIncludePaths :
            path.strip()
            if path != "" :
                LibPathList.append(path)
                # print(path)
        self.Args["LibPaths"] = LibPathList

        self.Args["VCRuntime"] = FirstSplitedCmd[8].strip()

    def exec(self) :
        if self.IsBuild == True :
            RunBuild(self.Args)
        elif self.IsRebuild == True :
            RunRebuild(self.Args)
        else :
            RunClean()
