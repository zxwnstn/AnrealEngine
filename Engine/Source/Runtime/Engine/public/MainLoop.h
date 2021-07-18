#pragma once

#include "Engine.h"

class MainLoop
{
public:
	MainLoop();

public:
	void Init();
	void Tick(float deltaTime);

private:
	bool IsInitiated;
};

