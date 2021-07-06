#pragma once

#include <string>
#include <unordered_map>
#include <iostream>
#include <stack>
#include <memory>

#ifdef _WIN32
	#define EXPORT __declspec(dllexport)
	#define IMPORT __declspec(dllimport)
#endif