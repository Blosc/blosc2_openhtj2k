# Blosc - Blocked Shuffling and Compression Library
#
# Copyright (C) 2023  The Blosc Developers <blosc@blosc.org>
# https://blosc.org
# License: BSD 3-Clause (see LICENSE.txt)
#
# See LICENSE.txt for details about copyright and rights to use.

# Build OpenHTJ2K statically
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_subdirectory(OpenHTJ2K)

# Build libblosc2_openhtj2k.so
add_library(blosc2_openhtj2k MODULE blosc2_htj2k.cpp)

if(MSVC OR MINGW)
    # Necessary for compiling blosc2_openhtj2k.lib
    set_property(TARGET blosc2_openhtj2k PROPERTY WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()

include_directories(
    OpenHTJ2K/source/apps/decoder
    OpenHTJ2K/source/core/interface
)

link_directories(${Python_LIB})
target_link_libraries(blosc2_openhtj2k open_htj2k)

# Install
install(TARGETS blosc2_openhtj2k LIBRARY DESTINATION blosc2_openhtj2k)

# Test program
add_executable(test_j2k test_j2k.c utils.cpp)
if(MSVC OR MINGW)
   target_link_libraries(test_j2k blosc2 open_htj2k)
else()
   target_link_libraries(test_j2k blosc2 open_htj2k m)
endif()
