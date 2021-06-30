import os

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

class BuildDesc :
    def __init__(self) :
        self.ModuleName = ""
        self.DependencyList = []
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

        buildcommands 
        {
            "../../Engine/Scripts/Build.bat -$(Configuration) -$(VC_IncludePath) -$(WindowsSDK_IncludePath) -$(VC_LibraryPath_x64) -$(WindowsSDK_LibraryPath_x64)"
        }

        rebuildcommands 
        {
            "../../Engine/Scripts/Rebuild.bat -$(Configuration) -$(VC_IncludePath) -$(WindowsSDK_IncludePath) -$(VC_LibraryPath_x64) -$(WindowsSDK_LibraryPath_x64)"
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