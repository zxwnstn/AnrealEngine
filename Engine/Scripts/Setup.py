import os
import sys
import Anreal

#global
RootDir = Anreal.GetAnrealRootDir()
def CreateGenerateProjectFiles() :
    ConfigsPath = RootDir + "/Engine/Configs"
    SetupFile = "Setup.ini"
    Setup = Anreal.INIReader(ConfigsPath, SetupFile)

    Generate_bat = open("GenerateProjectFiles.bat", 'w')
    Generate_bat.write("Engine\Extras\ThirdParty\premake5\premake5.exe " + Setup.GetValue("Target") + " ")
    Generate_bat.close()

def GenerateLuaScript() :

    LuaScript = open("premake5.lua", 'w')
    LuaScript.write(Anreal.PremakeBasicScript)
    LuaScript.close()

def main() :
    CreateGenerateProjectFiles()
    GenerateLuaScript()

if __name__ == '__main__':
    os.chdir(RootDir)
    main()
