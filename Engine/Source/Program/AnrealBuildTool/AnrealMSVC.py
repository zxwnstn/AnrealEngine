import os
import sys
import Anreal
import AnrealConfigMapper

def CreateClCmdLine(args, clOptions, description, sources) :
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

    #Attach cpp files that will be compile
    for Cpp in sources :
        ClCmdLine += ' ' + Cpp

    #Attach native build options
    for clOpt in clOptions :
        ClCmdLine += ' ' + clOpt

    return ClCmdLine

def CreateLinkCmdLine(args, linkOptions, description, objs, objsPath, binPath) :
    
    LinkCmdLine = ""
    
    Config = args["Config"]
    LinkPath = args["VCRuntime"]
    Index = LinkPath.find('\\')
    LinkPath = LinkPath[:Index] + '\"' + LinkPath[Index:]

    #Choose lib.exe or link.exe
    if Config == "ShippingGame" or Config == "ShippingEditor" :
        LinkCmdLine = LinkPath + "\"" + "/lib.exe"
    else :
        LinkCmdLine = LinkPath + "\"" + "/link.exe"

    #Add Module Lib Path
    LibPaths = args["LibPaths"]
    for LibPath in LibPaths:
        LinkCmdLine += " /LIBPATH:\"" + LibPath + "\""
    LinkCmdLine += " /LIBPATH:\"" + binPath + "\""

    #Attach obj files that will be link
    for obj in objs :
       LinkCmdLine += " \"" + objsPath + '/' + obj + ".obj\""

    #Attach dependency


    #Attach native build options
    # for linkOpt in linkOptions :
    #    LinkCmdLine += ' ' + linkOpt
    LinkCmdLine += " /DLL /DEBUG /PDB:" + description.ModuleName + ".pdb"

    LinkCmdLine += " /nologo "

    return LinkCmdLine

def PromptBuildModule(args, nativeBuildOptions, description) :

    Sources = []
    Anreal.GatherFilesFromRecursiveIterate(Sources, description.ModulePath, "cpp")
    
    ObjsPath = Anreal.ObjPath + "/" + args["Config"] + "/" + args["Compiler"]
    Anreal.TryCreatePath(ObjsPath)
    os.chdir(ObjsPath)
    CLCommandLine = CreateClCmdLine(args, nativeBuildOptions["CL"], description, Sources)
    os.system(CLCommandLine)

    Objs = []
    Anreal.GatherOnlyFileNameFromSourceList(Sources, Objs)

    BinPath = Anreal.BinPath + "/" + args["Config"] + "/" + args["Compiler"]
    Anreal.TryCreatePath(BinPath)
    os.chdir(BinPath)
    LinkCommandLine = CreateLinkCmdLine(args, nativeBuildOptions["Link"], description, Objs, ObjsPath, BinPath)
    os.system(LinkCommandLine)

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

def PromptBuildProgram(args, program) :
    ProgramPath = Anreal.RootPath + "/Engine/Source/" +  program
    Modules = os.listdir(ProgramPath)

    ConfigMapper = AnrealConfigMapper.GetConfigMapper(args["Compiler"])
    NativeBuildOptions = ConfigMapper.ParseAndGetMappedBuildOptions(args["Config"])

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
    i = 0
    for Description in OrdererdBuildDescList :
        if i != 0 :
            break
        PromptBuildModule(args, NativeBuildOptions, Description)
        i += 1

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
        FullIncludePath = FirstSplitedCmd[4] + ';' + FirstSplitedCmd[5]
        TokkenizedIncludePaths = FullIncludePath.split(';')
        for path in TokkenizedIncludePaths :
            path = path.strip()
            if path != "" :
                IncludePathList.append(path)
        self.Args["IncludePaths"] = IncludePathList

        # Forth - Fill lib path with exactly tokkenized paths FirstSplitedCmd[6], FirstSplitedCmd[7]
        LibPathList = []
        FullLibPath = FirstSplitedCmd[6] + ';' + FirstSplitedCmd[7]
        TokkenizedIncludePaths = FullLibPath.split(';')
        for path in TokkenizedIncludePaths :
            path = path.strip()
            if path != "" :
                LibPathList.append(path)
        self.Args["LibPaths"] = LibPathList

        self.Args["VCRuntime"] = FirstSplitedCmd[8].strip()

    def exec(self) :
        if self.IsBuild == True :
            RunBuild(self.Args)
        elif self.IsRebuild == True :
            RunRebuild(self.Args)
        else :
            RunClean()
