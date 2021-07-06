#pragma once

#include "PublicPCH/pch.h"

#ifdef RHI_IMPL
	#define RHI_API EXPORT
#else
	#define RHI_API IMPORT
#endif