import os
import sys
import Anreal

Target = sys.argv[1]
os.chdir(Anreal.RootPath)

if Target == 'vs2019' :
	ProjectFile = open("Projects/Engine/Engine.vcxproj.user", 'w')
	ProjectFile.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
	ProjectFile.write("<Project ToolsVersion=\"Current\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\">\n")

	for Config in Anreal.ConfigLists :
		BinFile = Anreal.BinPath + '/' + Config + '/' + Target + '/'
		if Config.endswith("Editor") :
			BinFile += "AnrealEditor.exe"

		ProjectFile.write("\t<PropertyGroup Condition=\"\'$(Configuration)|$(Platform)\'==\'" + Config + "|x64\'\">\"\n")
		ProjectFile.write("\t\t<LocalDebuggerCommand>" + BinFile + "</LocalDebuggerCommand>\n")
		ProjectFile.write("\t\t<DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>\n")
		ProjectFile.write("\t</PropertyGroup>\n")
	ProjectFile.write("</Project>\n")
