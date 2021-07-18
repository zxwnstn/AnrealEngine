#include "MainLoop.h"
#include "Core/public/Platform/Window.h"

FWindow* MainWindow;

MainLoop::MainLoop()
	: IsInitiated(false)
{
}


void MainLoop::Init()
{
	if (IsInitiated)
	{
		return;
	}

	FWindow::FWindowBasicInform MainWindowInform;
	MainWindowInform.Parent = nullptr;
	MainWindowInform.Width = 1280;
	MainWindowInform.Height = 720;
	MainWindowInform.WindowName = TEXT("Anreal Main Window");

	MainWindow = FWindow::Create(MainWindowInform);
	MainWindow->Init();
	MainWindow->RegisterWindow();
	MainWindow->Show();

	IsInitiated = true;
}

void MainLoop::Tick(float deltaTime)
{
}

MainLoop LoopInst;
