#pragma once

#include "PublicPCH/pch.h"

#ifdef RENDERER_IMPL
	#define RENDERER_API EXPORT
#else
	#define RENDERER_API IMPORT
#endif