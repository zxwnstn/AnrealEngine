#include "PublicPCH/pch.h"
#include "ModuleManager.h"

ModuleManager::ModuleManager()
{
}

ModuleManager * ModuleManager::Get()
{
	static ModuleManager* Inst = nullptr;
	if (Inst)
	{
		Inst = new ModuleManager;
	}
	return Inst;
}

void ModuleManager::ShotDown()
{
	for (auto& Moudle : ModuleInstList)
	{
		Moudle.second->DestroyInst();
	}
}


void ModuleManager::Init(const std::vector<Name>& list)
{
}

IModule * ModuleManager::GetModule(NameRef moduleName)
{
	return nullptr;
}

void ModuleManager::AddModule(NameRef moduleName)
{
}

void ModuleManager::LoadModule(NameRef moduleName)
{
}

void ModuleManager::UnLoadModule(NameRef moduleName)
{
}

void IModule::DestroyInst()
{
}
