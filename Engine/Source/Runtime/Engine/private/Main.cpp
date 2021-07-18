#include "PublicPCH/pch.h"
#include "Main.h"
#include "MainLoop.h"

#include "Core/public/Type.h"

extern MainLoop LoopInst;

int Run()
{
	while (true)
	{
		float DeltaTime = 1.0f;//Ticker::GetTickTime();
		LoopInst.Tick(DeltaTime);
	}
	return 0;
}

int EngineMain(int argc, char* argv[])
{
	LoopInst.Init();
	int ExitCode = Run();

	return ExitCode;
}

