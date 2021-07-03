import os
import sys
import Anreal
sys.path.append(Anreal.BuildToolPath)

def GetBuildCmdList() :
    FirstSplitedCmd = []
    MergedCmd = ""
    for cmd in sys.argv :
        MergedCmd += cmd + ' '
    FirstSplitedCmd = MergedCmd.split('-')

    Compiler = FirstSplitedCmd[2].strip()
    if Compiler == "vs2017" or Compiler == "vs2019" :
        import AnrealMSVC
        return AnrealMSVC.MSCVBuildCmdList(FirstSplitedCmd)

def main() :
    os.chdir(Anreal.RootPath)
    CmdList = GetBuildCmdList()
    CmdList.exec()

if __name__ == '__main__':
    main()
