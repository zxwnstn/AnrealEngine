#pragma once

#include "PublicPCH/pch.h"

#ifdef ENGINE_IMPL
	#define ENGINE_API EXPORT
#else
	#define ENGINE_API IMPORT
#endif