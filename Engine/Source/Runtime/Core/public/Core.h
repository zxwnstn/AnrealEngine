#pragma once

#include "PublicPCH/pch.h"

#ifdef CORE_IMPL
	#define CORE_API EXPORT
#else
	#define CORE_API IMPORT
#endif
