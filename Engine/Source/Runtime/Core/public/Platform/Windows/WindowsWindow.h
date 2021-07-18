#pragma once

#ifdef _WIN32

#include "Platform/Window.h"

class FWindowsWindow : public FWindow
{
private:
	FWindowsWindow(const FWindowBasicInform& inform);
	~FWindowsWindow();

public:
	void Init() override;
	void Show() override;
	void Hide() override;

private:
	void RegisterWindow();

private:
	friend class FWindow;

	WNDCLASS WndClass;
	bool Registered = false;
};

#endif