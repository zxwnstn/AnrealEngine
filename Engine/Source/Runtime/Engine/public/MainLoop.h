#pragma once

#include "Engine.h"

class MainLoop
{
private:
	MainLoop();
	void InitImpl();

public:
	void Init();
	void Tick(float deltaTime);

};

ENGINE_API int GetSome();