class INIReader :
    Data = {}
    FileName = ""
    Path = ""
    def __init__(self, path, fileName) :
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

ScriptBasic = """
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
	    location "ProjectFiles/Engine"
	    kind "Makefile"
	    language "C++"

        buildcommands 
        {
            "../../Engine/Scripts/Build.bat"
        }

        rebuildcommands 
        {
            "../../Engine/Scripts/Rebuild.bat"
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
"""