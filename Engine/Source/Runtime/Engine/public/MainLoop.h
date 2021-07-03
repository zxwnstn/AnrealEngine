#pragma once

class MainLoop
{
private:
	MainLoop();
	void InitImpl();

public:
	void Init();
	void Tick(float deltaTime);


};

MainLoop* LoopInst = nullptr;