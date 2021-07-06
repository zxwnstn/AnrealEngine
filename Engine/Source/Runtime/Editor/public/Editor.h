#pragma once

#include "PublicPCH/pch.h"

#ifdef EDITOR_IMPL
	#define EDITOR_API EXPORT
#else
	#define EDITOR_API IMPORT
#endif