#pragma once

#include "PublicPCH/pch.h"

#ifdef D3D12RHI_IMPL
	#define D3D12RHI_API EXPORT
#else
	#define D3D12RHI_API IMPORT
#endif
