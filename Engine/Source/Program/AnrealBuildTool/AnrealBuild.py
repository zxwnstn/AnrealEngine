import os
import sys
import Anreal
sys.path.append(Anreal.BuildToolPath)
import AnrealMSVC
import AnrealBuilder

def GetBuilder() :
    FirstSplitedCmd = []
    MergedCmd = ""
    for cmd in sys.argv :
        MergedCmd += cmd + ' '
    FirstSplitedCmd = MergedCmd.split('-')

    Compiler = FirstSplitedCmd[2].strip()
    if Compiler == "vs2017" or Compiler == "vs2019" :
        import AnrealMSVC
        return AnrealMSVC.MSCVBuilder(FirstSplitedCmd)

def main() :
    os.chdir(Anreal.RootPath)
    Builder = GetBuilder()
    Builder.exec()

if __name__ == '__main__':
    main()
