import os
import sys
import Anreal
import AnrealBuilder

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
    for Dependency in description.DependencyList :
        LinkCmdLine += " " + Dependency + ".lib"

    #Attach native build options
    for linkOpt in linkOptions :
        LinkCmdLine += ' ' + linkOpt
        if linkOpt.endswith('/PDB:') :
            LinkCmdLine += description.ModuleName + '.pdb' 
    LinkCmdLine += " /nologo"

    #Set output
    if description.Executable == False :
        LinkCmdLine += " /OUT:" + description.ModuleName
        if Config == "ShippingGame" or Config == "ShippingEditor" :
            LinkCmdLine += ".lib"
            pass
        else :
            LinkCmdLine += ".dll /DLL"
    else :
        LinkCmdLine += " /OUT:" + "AnrealEditor.exe"

    return LinkCmdLine

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

    #Add identity macro
    UpperModuleName = description.ModuleName.upper()
    ClCmdLine += " /D\"" + UpperModuleName + "_IMPL\""

    #Attach native build options
    for clOpt in clOptions :
        ClCmdLine += ' ' + clOpt
    ClCmdLine += " /nologo"

    return ClCmdLine

class MSCVBuilder(AnrealBuilder.BasicBuilder) :
    def __init__(self, FirstSplitedCmd) :
        # MSVC cmd legend (indicate FirstSplitedCmd)
        # 0 - Exec argument
        # 1 - BuildType
        # 2 - Config
        # 3, 4 - Basic Include path
        # 5, 6 - Basic Lib path 
        AnrealBuilder.BasicBuilder.__init__(self)

        # First - Set build type and erase elm unnecessaries
        BuildType = FirstSplitedCmd[1].strip()
        if BuildType == "Build" :
            self.IsBuild = True
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

    
    def PromptBuildModule(self, args, nativeBuildOptions, description) :
        Sources = []
        Anreal.GatherFilesFromRecursiveIterate(Sources, description.ModulePath, "cpp")
    
        ObjsPath = Anreal.ObjPath + "/" + args["Compiler"] + "/" + args["Config"] 
        Anreal.TryCreatePath(ObjsPath)
        os.chdir(ObjsPath)
        CLCommandLine = CreateClCmdLine(args, nativeBuildOptions["CL"], description, Sources)
        os.system(CLCommandLine)

        Objs = []
        Anreal.GatherOnlyFileNameFromSourceList(Sources, Objs)

        BinPath = Anreal.BinPath + "/" + args["Compiler"] + "/" + args["Config"]
        Anreal.TryCreatePath(BinPath)
        os.chdir(BinPath)
        LinkCommandLine = CreateLinkCmdLine(args, nativeBuildOptions["Link"], description, Objs, ObjsPath, BinPath)
        os.system(LinkCommandLine)
