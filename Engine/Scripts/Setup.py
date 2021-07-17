import os
import sys
import Anreal

#global
def CreateGenerateProjectFiles(setup) :
    Generate_bat = open("GenerateProjectFiles.bat", 'w')
    Generate_bat.write("Engine\Extras\ThirdParty\premake5\premake5.exe " + setup.GetValue("Target") + "\n")
    Generate_bat.close()

def GenerateLuaScript(setup) :
    LuaScript = open("premake5.lua", 'w')
    LuaScript.write(Anreal.GetPremakeScript(setup.GetValue("Target")))
    LuaScript.close()

def main() :
    Setup = Anreal.INIReader(Anreal.ConfigPath + "", "Setup.ini")
    CreateGenerateProjectFiles(Setup)
    GenerateLuaScript(Setup)

if __name__ == '__main__':
    os.chdir(Anreal.RootPath)
    main()
