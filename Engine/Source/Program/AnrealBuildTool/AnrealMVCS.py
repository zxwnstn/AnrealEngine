import os
import sys
import Anreal

def ParseAndGetClCmdLine(args, description) :
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
        ClCmdLine += " /I " +  "\"" + includePath + "\""

    #Add Module Include Path
    ClCmdLine += " /I " +  "\"" + description.ProgramPath + "\""

    return ClCmdLine

def ParseAndGetLinkCmdLine(args, description) :
    return ""