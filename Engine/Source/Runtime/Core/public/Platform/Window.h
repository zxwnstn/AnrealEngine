#pragma once

#include "Type.h"

struct FWindowHandle;

class CORE_API FWindow
{
public:
	struct FWindowBasicInform
	{
		Uint32 Width = 0;
		Uint32 Height = 0;
		TString WindowName;
		FWindow* Parent = nullptr;
		TArray<FWindow*> Childs;
	};

protected:
	FWindow::FWindow(const FWindowBasicInform& inform)
		: Inform(inform)
	{}

public:
	virtual ~FWindow() 
	{
		for (FWindow* Child : Inform.Childs)
		{
			delete Child;
		}
		delete Handle;
	}

public:
	static FWindow* Create(const FWindowBasicInform& prop);
	virtual void Init() = 0;
	virtual void Show() = 0;
	virtual void Hide() = 0;

	FWindowHandle* GetHandle() const { return Handle; }

protected:
	FWindowBasicInform Inform;
	FWindowHandle* Handle;
};