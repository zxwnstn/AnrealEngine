import os
import json

def GetAnrealRootDir() :
    Ret = os.getcwd()
    StrList = Ret.split('\\')
    Rootindex = len(StrList) - 4
    Index = 0
    RootPath = ""
    
    for i in StrList:
        if Index == Rootindex:
            break
        Slash = "/"
        if Index == Rootindex- 1:
            Slash = ""
        RootPath += i + Slash
        Index = Index + 1

    Ret = RootPath
    return Ret

def TryCreatePath(path) :
    if os.path.exists(path) : 
        return
    os.makedirs(path)

def GatherFilesFromRecursiveIterate(inOutFiles, path, desiredExtension) :
    ListDir = os.listdir(path)
    for candidate in ListDir :
        if os.path.isfile(path + '/' + candidate) == True :
            if candidate.endswith(desiredExtension) :
                inOutFiles.append(path + '/' + candidate)
        elif os.path.isdir(path + '/' + candidate) == True :
            GatherFilesFromRecursiveIterate(inOutFiles, path + '/' + candidate, desiredExtension)

def GatherOnlyFileNameFromSourceList(inSources, outNameList) :
    for Source in inSources :
        s = os.path.splitext(Source)
        s = os.path.split(s[0])
        outNameList.append(s[1])

class BuildDesc :
    def __init__(self) :
        self.ModuleName = ""
        self.ModulePath = ""
        self.ProgramPath = ""
        self.DependencyList = []
        self.Executable = False
        self.SetDependency()
        self.SetOther()
    
    def SetDependency(self) :
        pass
    
    def SetOther(self) :
        pass

class INIReader :
    def __init__(self, path, fileName) :
        self.Data = {}
        self.FileName = fileName
        self.Path = path
        File = open(path + '/' + fileName, 'r')
        print("INIReader::Read file : {0}".format(self.FileName))
        Lines = File.readlines()
        i = 0  
        for Line in Lines :
            i += 1
            Tokkens = Line.split('=')
            Count = Tokkens.__len__()
            if Count == 0 :
                continue 
            if Count > 2 :
                print("{0} line {1} {2} : ini file seems not to be appropriate format".format(fileName, i, Line))
                continue
            self.Data[Tokkens[0]] = Tokkens[1].strip()
        File.close()
    
    def GetValue(self, key) :
        Ret = self.Data.get(key)
        if Ret == None :
            print("There is no {0} variable on ini file".format(key))
        return self.Data.get(key)

    def GetValues(self) :
        return self.Data.values()

    def GetKeys(self) :
        return self.Data.keys()

class ConfigMapper :
    def __init__(self) :
        self.Compiler = ""
        self.NativeBuildOptions = {}
        self.AbstractedOptions = []
        pass
    
    def MapNativeBuildOpt(self) :
        pass

    def GatherAbstractedBuildOptions(self, config) :
        with open(ConfigPath + "/Build/EngineConfig.json") as EngineConfigJson :
            EngineConfigs = json.load(EngineConfigJson)
    
        self.AbstractedOptions= EngineConfigs[config]
        CommonOptions= EngineConfigs["Common"]
        for CommonOption in CommonOptions :
            self.AbstractedOptions.append(CommonOption)

    def ParseAndGetMappedBuildOptions(self, config) :
        self.GatherAbstractedBuildOptions(config)
        self.MapNativeBuildOpt()
        return self.NativeBuildOptions

RootPath = GetAnrealRootDir()
BinPath = RootPath + "/Engine/Binaries/"
BuildToolPath = RootPath + "/Engine/Source/Program/AnrealBuildTool"
ConfigPath = RootPath + "/Engine/Configs"
ObjPath = RootPath + "/Engine/Objs"
ConfigLists = ["DebugEditor", "DebugGame", "DevelopEditor", "DevelopGame", "ShippingEditor", "ShippingGame"]

PremakeBasicScript = """
workspace "Anreal"
    configurations
	{
		"DebugEditor",
		"DebugGame",
        "DevelopEditor",
		"DevelopGame",
        "ShippingEditor",
		"ShippingGame"
	}
	platforms
	{
	    "x64"
	}
    characterset ("Unicode")
	startproject "Engine"
    filter "system:windows"
	cppdialect "C++17"

    group "Engine"
        project "Engine"
	    location "Projects/Engine"
	    kind "Makefile"
	    language "C++"
        cppdialect "C++17"

        buildcommands 
        {
            {0}
        }

        rebuildcommands 
        {
            {1}
        }
        
        cleancommands 
        {
            "../../Engine/Scripts/Clean.bat"
        }

	    files
	    {
		    "Engine/Source/Runtime/**.h",
		    "Engine/Source/Runtime/**.cpp",
            "Engine/Source/Runtime/**.py"
        }

        includedirs
	    {
		    "Engine/Source/Runtime/",
            "Engine/Source/Runtime/*/public"
	    }

    group ""

    group "Program"
        project "AnrealBuildTool"
	    location "Projects/Program/AnrealBuildTool"
	    kind "Makefile"
	    language "C++"

        vpaths 
        {
            ["Source"] = "Engine/Source/Program/AnrealBuildTool",
            ["Script"] = "Engine/Scripts",
            ["AnrealPythonCore"] = "Engine/Extras/ThirdParty/Python/Lib"
        }

	    files
	    {
		    "Engine/Source/Program/AnrealBuildTool/**.py",
            "Engine/Extras/ThirdParty/Python/Lib/Anreal.py",
            "Engine/Scripts/**.bat",
            "Engine/Scripts/**.py"
        }
    group ""
"""

VS2017CommandLines = ["\"../../Engine/Scripts/Build.bat -vs2017 -$(Configuration) -$(VC_IncludePath) -$(WindowsSDK_IncludePath) -$(VC_LibraryPath_x64) -$(WindowsSDK_LibraryPath_x64) -$(VC_PGO_RunTime_Dir)\"", "\"../../Engine/Scripts/Rebuild.bat -vs2019 -$(Configuration) -$(VC_IncludePath) -$(WindowsSDK_IncludePath) -$(VC_LibraryPath_x64) -$(WindowsSDK_LibraryPath_x64) -$(VC_PGO_RunTime_Dir)\""]
VS2019CommandLines = ["\"../../Engine/Scripts/Build.bat -vs2019 -$(Configuration) -$(VC_IncludePath) -$(WindowsSDK_IncludePath) -$(VC_LibraryPath_x64) -$(WindowsSDK_LibraryPath_x64) -$(VC_PGO_RunTime_Dir)\"", "\"../../Engine/Scripts/Rebuild.bat -vs2019 -$(Configuration) -$(VC_IncludePath) -$(WindowsSDK_IncludePath) -$(VC_LibraryPath_x64) -$(WindowsSDK_LibraryPath_x64) -$(VC_PGO_RunTime_Dir)\""]

def GetPremakeScript(target) :
    Script = PremakeBasicScript
    if target == "vs2017" :
        Script = Script.replace("{0}", VS2017CommandLines[0])
        Script = Script.replace("{1}", VS2017CommandLines[0])
    if target == "vs2019" :
        Script = Script.replace("{0}", VS2019CommandLines[0])
        Script = Script.replace("{1}", VS2019CommandLines[0])

    return Script