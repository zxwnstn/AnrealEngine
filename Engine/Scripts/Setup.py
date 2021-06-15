import os

class SetupINI :
    CMakeVer = 0 
    VSVer = 0 
    def __init__(self) :
        
        print("\n############ Hello AnrealEngine ############\n")

        print("initiation Setup properties...")

        Setup = open("Engine/Configs/Setup.ini", 'r')
        lines = Setup.readlines()
        for line in lines :
            split = line.split()
            for elm in split :
                if elm == "Target" :
                    index = line.rfind('=')
                    self.VSVer = line[index + 2: len(line) - 1]
                    continue
                if elm == "CMakeVersion" :
                    index = line.rfind('=')
                    self.CMakeVer = line[index + 2: len(line) - 1]
        print("Setted CMake Version : " + self.CMakeVer)
        print("Build target : " + self.GetVSVersionSTR())
        print()
        Setup.close()

    def GetVSVersionSTR(self) :
        if self.VSVer == "VS2019" :
            return "Visual Studio 16 2019"
        if self.VSVer == "VS2017" :
            return "Visual Studio 16 2017 Win64"
        raise Exception('Unknown Ver {0}', self.VSVer)

#globals
os.chdir("../../")
RootDir = os.getcwd()
EngineSource = "Engine/Source/"
SourceDir = RootDir + "/" + EngineSource
ini = SetupINI()

def GetDirList(dir) :
    os.chdir(dir)
    return os.listdir()

def CreateMainCMakeLists(moduleList) :
    global RootDir, EngineSource, ini
    
    os.chdir(RootDir)
    CMakeLists = open("CMakeLists.txt", 'w')
    CMakeLists.write("cmake_minimum_required(VERSION " + ini.CMakeVer + " FATAL_ERROR)\n")
    CMakeLists.write("project(Anreal LANGUAGES CXX)\n")
    CMakeLists.write("set_property(GLOBAL PROPERTY USE_FOLDERS ON)\n")
    for module in moduleList :
        CMakeLists.write("add_subdirectory(" + EngineSource + module + ")\n")
    CMakeLists.write("set_target_properties(\n")
    for module in moduleList :
        CMakeLists.write(module + '\n')
    CMakeLists.write("PROPERTIES\nFOLDER Engine\n)")
    CMakeLists.close()

def GetSourceList(OutList, moduleDir, NamePath) :
    DirList = os.listdir(moduleDir)
    for dir in DirList :
        index = dir.rfind('.')
        if index != -1 :
            ext = dir[index + 1 : len(dir)]
            if ext != "txt" : 
                if len(NamePath) != 0 :     
                    OutList.append(NamePath + '/' + dir)
                else :
                    OutList.append(dir)
        else : 
            if len(NamePath) != 0 :     
                GetSourceList(OutList, moduleDir + '/' + dir, NamePath + '/' + dir)
            else : 
                GetSourceList(OutList, moduleDir + '/' + dir, dir)

def CreateModuleCMakeLists(moduleName) :
    global RootDir, EngineSource
    ModuleDir = RootDir + '/' + EngineSource + moduleName
    os.chdir(ModuleDir)
    CMakeLists = open("CMakeLists.txt", "w")
    CMakeLists.write("project(" + moduleName + " LANGUAGES CXX)\n")
    
    OutList = []
    NamePath = ""
    print(moduleName)
    GetSourceList(OutList, ModuleDir, NamePath)

    CMakeLists.write("add_library(\n")
    CMakeLists.write("${PROJECT_NAME}\n")
    for source in OutList :
        CMakeLists.write( source + "\n")
    CMakeLists.write(")\n")

    CMakeLists.close()

def CreateCMakeFiles() :
    global RootDir, SourceDir, ini

    os.chdir(RootDir)

    Generate_bat = open("Generate.bat", 'w')
    Generate_bat.write("cmake -S. -B./build -G \"" + ini.GetVSVersionSTR() + "\"")
    Generate_bat.close()

    MouduleList = GetDirList(SourceDir)
    CreateMainCMakeLists(MouduleList)

    print("Find Modules....")
    for Name in MouduleList:
        CreateModuleCMakeLists(Name)

def main() :
    CreateCMakeFiles()

if __name__ == '__main__':
    main()