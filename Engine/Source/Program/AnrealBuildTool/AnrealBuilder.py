import os
import sys
import copy
import Anreal
import AnrealConfigMapper


class BasicBuilder :
    def __init__(self) :
        self.Args = {}
        self.IsBuild = False
        self.IsRebuild = False

    def PromptBuildModule(self, args, nativeBuildOptions, description) :
        pass

    def FindBuildDescAsName(self, moduleName, buildDesc) :
        for Description in buildDesc :
            if Description.ModuleName == moduleName :
                return Description

    def BuildOderingByDependencies(self, buildDescs) : 
        WorkList = copy.deepcopy(buildDescs)
        OrdererdBuildDescList = []

        while len(WorkList) != 0 :
            for Description in WorkList :
                if len(Description.DependencyList) == 0 :
                    CheckedModule = Description.ModuleName
                    OrdererdBuildDescList.append(self.FindBuildDescAsName(CheckedModule, buildDescs))
                    WorkList.remove(Description)
                    for Description in WorkList :
                        for Dependency in Description.DependencyList :
                            if Dependency == CheckedModule :
                                Description.DependencyList.remove(CheckedModule)
                                break

        return OrdererdBuildDescList

    def PromptBuildProgram(self, args, program) :
        ProgramPath = Anreal.RootPath + "/Engine/Source/" +  program
        Modules = os.listdir(ProgramPath)

        ConfigMapper = AnrealConfigMapper.GetConfigMapper(args["Compiler"])
        NativeBuildOptions = ConfigMapper.ParseAndGetMappedBuildOptions(args["Config"])
        
        BuildDescList = []
        for Module in Modules :
            if Module == "PublicPCH" :
                continue
            ModulePath = ProgramPath + '/' + Module
            sys.path.append(ModulePath)
            BuildScript = __import__(Module + "Build")
            Description = BuildScript.GetBuildDesc()
            Description.ProgramPath = ProgramPath
            Description.ModulePath = ModulePath
            BuildDescList.append(Description)
        
        OrdererdBuildDescList = self.BuildOderingByDependencies(BuildDescList)
        for Description in OrdererdBuildDescList :
            self.PromptBuildModule(args, NativeBuildOptions, Description)

    def RunBuild(self, args) :
        SourceDir = Anreal.RootPath + '/' + "Engine/Source" 
        ProgramCategories = os.listdir(SourceDir)
        for Program in ProgramCategories :
            if Program == "Program" : 
                continue
            self.PromptBuildProgram(args, Program)

    def RunClean(self) :
        pass

    def RunRebuild(self, args) :
        self.RunClean()
        self.RunBuild(args)

    def exec(self) :
        if self.IsBuild == True :
            self.RunBuild(self.Args)
        elif self.IsRebuild == True :
            self.RunRebuild(self.Args)
        else :
            self.RunClean()