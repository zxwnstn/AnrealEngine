import os
import sys
import Anreal

#global
RootDir = Anreal.GetAnrealRootDir()
AnrealPythonLibDir = "/Engine/Extras/ThirdParty/Python/Lib/Anreal"
sys.path.append(RootDir + AnrealPythonLibDir)
from AnrealUtil import INIReader
from AnrealUtil import ScriptBasic
def CreateGenerateProjectFiles() :
    ConfigsPath = RootDir + "/Engine/Configs"
    SetupFile = "Setup.ini"
    Setup = INIReader(ConfigsPath, SetupFile)

    Generate_bat = open("GenerateProjectFiles.bat", 'w')
    Generate_bat.write("Engine\Extras\ThirdParty\premake5\premake5.exe " + Setup.GetValue("Target") + " ")
    Generate_bat.write("PAUSE")
    Generate_bat.close()

def GenerateLuaScript() :

    LuaScript = open("premake5.lua", 'w')
    LuaScript.write(ScriptBasic)
    LuaScript.close()

def main() :
    CreateGenerateProjectFiles()
    GenerateLuaScript()

if __name__ == '__main__':
    os.chdir(RootDir)
    main()


# def GetDirList(dir) :
#     os.chdir(dir)
#     return os.listdir()

# def CreateMainCMakeLists(moduleList) :
#     global RootDir, EngineSource, ini
    
#     os.chdir(RootDir)
#     CMakeLists = open("CMakeLists.txt", 'w')
#     CMakeLists.write("cmake_minimum_required(VERSION " + ini.CMakeVer + " FATAL_ERROR)\n")
#     CMakeLists.write("project(Anreal LANGUAGES CXX)\n")
#     CMakeLists.write("set_property(GLOBAL PROPERTY USE_FOLDERS ON)\n")
#     for module in moduleList :
#         CMakeLists.write("add_subdirectory(" + EngineSource + module + ")\n")
#     CMakeLists.write("set_target_properties(\n")
#     for module in moduleList :
#         CMakeLists.write(module + '\n')
#     CMakeLists.write("PROPERTIES\nFOLDER Engine\n)")
#     CMakeLists.close()

# def GetSourceList(OutList, moduleDir, NamePath) :
#     DirList = os.listdir(moduleDir)
#     for dir in DirList :
#         index = dir.rfind('.')
#         if index != -1 :
#             ext = dir[index + 1 : len(dir)]
#             if ext != "txt" : 
#                 if len(NamePath) != 0 :     
#                     OutList.append(NamePath + '/' + dir)
#                 else :
#                     OutList.append(dir)
#         else : 
#             if len(NamePath) != 0 :     
#                 GetSourceList(OutList, moduleDir + '/' + dir, NamePath + '/' + dir)
#             else : 
#                 GetSourceList(OutList, moduleDir + '/' + dir, dir)

# def CreateModuleCMakeLists(moduleName) :
#     global RootDir, EngineSource
#     ModuleDir = RootDir + '/' + EngineSource + moduleName
#     os.chdir(ModuleDir)
#     CMakeLists = open("CMakeLists.txt", "w")
#     CMakeLists.write("project(" + moduleName + " LANGUAGES CXX)\n")
    
#     OutList = []
#     NamePath = ""
#     print(moduleName)
#     GetSourceList(OutList, ModuleDir, NamePath)

#     CMakeLists.write("add_library(\n")
#     CMakeLists.write("${PROJECT_NAME}\n")
#     for source in OutList :
#         CMakeLists.write( source + "\n")
#     CMakeLists.write(")\n")

#     CMakeLists.close()

# def main() :
#     CreateCMakeFiles()

# if __name__ == '__main__':
#     ini = INI.INIReader("sdf", "sdf")
#     main()