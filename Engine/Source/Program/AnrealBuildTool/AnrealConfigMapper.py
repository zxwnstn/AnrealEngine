import os
import sys
import Anreal
import json

class MSVC2019ConfigMapper(Anreal.ConfigMapper) :
    def __init__(self) :
        Anreal.ConfigMapper.__init__(self)
        self.Compiler = "vs2019"
    
    def MapNativeBuildOpt(self) :
        with open(Anreal.ConfigPath + "/Build/Platform/MSVC.json") as MSVCConfigJson :
            MSVCConfigs = json.load(MSVCConfigJson)
        
        self.NativeBuildOptions["CL"] = []
        self.NativeBuildOptions["Link"] = []
    
        CLOpts = MSVCConfigs[self.Compiler]["CL"]
        LinkOpts = MSVCConfigs[self.Compiler]["Link"]

        for AbstractedOption in self.AbstractedOptions :
            if AbstractedOption in CLOpts :
                self.NativeBuildOptions["CL"].append(CLOpts[AbstractedOption])
            elif AbstractedOption in LinkOpts :
                self.NativeBuildOptions["Link"].append(LinkOpts[AbstractedOption])
     
def GetConfigMapper(Compiler) :
    if Compiler == "vs2019" : 
        return MSVC2019ConfigMapper()