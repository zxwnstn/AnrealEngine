#include "Main.h"
#include "MainLoop.h"

extern MainLoop* LoopInst;

int Run()
{
	while (!RequestedExit())
	{
		float DeltaTime = 1.0f;//Ticker::GetTickTime();
		LoopInst->Tick(DeltaTime);
	}
	return GetExitCode();
}

int EngineMain(int argc, char* argv[])
{
	LoopInst->Init();
	int ExitCode = Run();

	return ExitCode;
}

