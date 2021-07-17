#pragma once

#include <string>
#include <unordered_map>
#include <iostream>
#include <stack>
#include <memory>

#ifdef _WIN32
	#ifndef SHIPPING_BUILD
		#define EXPORT __declspec(dllexport)
		#define IMPORT __declspec(dllimport)
	#else
		#define EXPORT
		#define IMPORT
	#endif
#endif