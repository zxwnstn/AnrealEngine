#ifdef _WIN32

#include "PublicPCH/pch.h"
#include "Platform/Windows/WindowsWindow.h"

struct FWindowHandle
{
	HWND NativeHandle = NULL;
};

//TODO : PlatformMisc::GetApplicationHandle()
static HINSTANCE HInst = GetModuleHandle(NULL);

FWindowsWindow::FWindowsWindow(const FWindowBasicInform& inform)
	: FWindow(inform)
{
	ZeroMemory(&WndClass, sizeof(WndClass));
	Handle = new FWindowHandle;
}

FWindowsWindow::~FWindowsWindow()
{
	UnregisterClass(Inform.WindowName.c_str(), HInst);
	CloseHandle(Handle->NativeHandle);
	delete Handle;
}

LRESULT __stdcall WndProc(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam)
{
	switch (iMessage)
	{
	case WM_MOUSEMOVE:
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	case WM_SIZE:
		break;
	default:
		break;
	}
	return (DefWindowProc(hWnd, iMessage, wParam, lParam));
}

void FWindowsWindow::Init()
{
	WndClass.cbClsExtra = 0;
	WndClass.cbWndExtra = 0;
	WndClass.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
	WndClass.hCursor = LoadCursor(NULL, IDC_ARROW);
	WndClass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	WndClass.hInstance = HInst;
	WndClass.lpszClassName = Inform.WindowName.c_str();
	WndClass.lpfnWndProc = WndProc;
	WndClass.lpszMenuName = NULL;
	WndClass.style = CS_HREDRAW | CS_VREDRAW;
	RegisterWindow();

	Handle->NativeHandle = CreateWindow(
		Inform.WindowName.c_str(),
		Inform.WindowName.c_str(),
		WS_OVERLAPPEDWINDOW,
		100,
		100,
		Inform.Width,
		Inform.Height,
		Inform.Parent ? Inform.Parent->GetHandle()->NativeHandle : NULL,
		NULL,
		HInst,
		NULL
	);

	RECT rc{ 0, 0, (LONG)Inform.Width, (LONG)Inform.Height };
	AdjustWindowRect(&rc, WS_CAPTION | WS_SYSMENU, false);
	SetWindowPos(Handle->NativeHandle, NULL, 0, 0, (rc.right - rc.left), (rc.bottom - rc.top), SWP_NOZORDER);
}

void FWindowsWindow::Show()
{
	assert(Registered);
	ShowWindow(Handle->NativeHandle, SW_SHOWNORMAL);
}

void FWindowsWindow::Hide()
{
}

void FWindowsWindow::RegisterWindow()
{
	if (Registered)
	{
		return;
	}

	RegisterClass(&WndClass);
	Registered = true;
}

FWindow* FWindow::Create(const FWindowBasicInform& inform)
{
	return new FWindowsWindow(inform);
}

#endif
