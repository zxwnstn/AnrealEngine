#pragma once

#include "Core.h"
#include "PublicPCH/pch.h"

#include "Platform/Windows/WindowsType.h"

using Name = std::string;
using NameRef = const std::string&;
using FString = std::string;
using FWString = std::wstring;

#ifdef UNICODE
	using TString = FWString;
#else
	using TString = FString;
#endif

template<typename T>
using TArray = std::vector<T>;
