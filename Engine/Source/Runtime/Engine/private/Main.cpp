#include "PublicPCH/pch.h"
#include "Main.h"
#include "MainLoop.h"

#include "Core/public/Type.h"

extern MainLoop* LoopInst;

int Run()
{
	while (false)
	{
		float DeltaTime = 1.0f;//Ticker::GetTickTime();
		LoopInst->Tick(DeltaTime);
	}
	std::cout << "Hello world And" << GetTypeID();
	return 0;
}

int EngineMain(int argc, char* argv[])
{
	LoopInst->Init();
	int ExitCode = Run();

	return ExitCode;
}

