#pragma once

#include "Core.h"
#include "Type.h"

class IModule
{
public:
	virtual IModule* CreateInstance() = 0;
	virtual void DestroyInst();
};

class ModuleManager
{
private:
	ModuleManager();

public:
	ModuleManager* Get();
	void ShotDown();

public:
	CORE_API void Init(const std::vector<Name>& list);
	
	IModule* GetModule(NameRef moduleName);
	
	void AddModule(NameRef moduleName);
	
	void LoadModule(NameRef moduleName);
	void UnLoadModule(NameRef moduleName);

private:
	static std::unordered_map<Name, IModule*> ModuleInstList;
};

#define DECLARE_MODULE(MODULE_NAME)					\
class ModuleInterface##_MODULE_NAME					\
{													\
public:												\
	static IModule* CreateInstance()				\
	{												\
		static MODULE_NAME* Inst = nullptr;			\
		if (!Inst)									\
		{											\
			Inst = new MODULE_NAME;					\
		}											\
		return Inst;								\
	}												\
};	