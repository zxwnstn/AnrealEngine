#include "MainLoop.h"

MainLoop::MainLoop()
{
}

void MainLoop::InitImpl()
{
}

void MainLoop::Init()
{
	InitImpl();
}

void MainLoop::Tick(float deltaTime)
{
}

MainLoop* LoopInst;

ENGINE_API int GetSome()
{
	return 11;
}