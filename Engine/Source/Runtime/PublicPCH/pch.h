#pragma once

// Standard
#include <string>
#include <unordered_map>
#include <iostream>
#include <stack>
#include <memory>
#include <cassert>

// Platform specific
#ifdef _WIN32
	#include <Windows.h>
	#pragma comment(lib, "Kernel32.lib")
	#pragma comment(lib, "Gdi32.lib")
	#pragma comment(lib, "User32.lib")
#endif


#ifndef SHIPPING_BUILD
	#ifdef _WIN32
		#define EXPORT __declspec(dllexport)
		#define IMPORT __declspec(dllimport)
	#endif 
#else
	#define EXPORT
	#define IMPORT
#endif
