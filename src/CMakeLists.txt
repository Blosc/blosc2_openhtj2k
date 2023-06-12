# Blosc - Blocked Shuffling and Compression Library
#
# Copyright (C) 2023  The Blosc Developers <blosc@blosc.org>
# https://blosc.org
# License: BSD 3-Clause (see LICENSE.txt)
#
# See LICENSE.txt for details about copyright and rights to use.

add_subdirectory(OpenHTJ2K)

include_directories(
    ${Python_INCLUDE}
    OpenHTJ2K/source/core/interface OpenHTJ2K/source/apps/decoder
    OpenHTJ2K/source/core/common OpenHTJ2K/source/core/codestream
    OpenHTJ2K/source/core/coding OpenHTJ2K/source/core/jph
    OpenHTJ2K/source/core/transform
)

if(MSVC OR MINGW)
    add_library(blosc2_openhtj2k MODULE blosc2_htj2k.cpp)
    # Necessary for compiling blosc2_openhtj2k.lib
    set_property(TARGET blosc2_openhtj2k PROPERTY WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
elseif (APPLE)
    add_library(blosc2_openhtj2k MODULE blosc2_htj2k.cpp)
else()
    add_library(blosc2_openhtj2k SHARED blosc2_htj2k.cpp)
endif()

link_directories(${Python_LIB})
target_link_libraries(blosc2_openhtj2k open_htj2k)

# This is needed for finding sibling libraries in the same directory for MacOS and Linux
# TODO: Figure out how to do that in Windows
if(APPLE)
    set_target_properties(blosc2_openhtj2k PROPERTIES INSTALL_RPATH "@loader_path/.")
elseif(UNIX)
    set_target_properties(blosc2_openhtj2k PROPERTIES INSTALL_RPATH "\${ORIGIN}/.")
endif()

install(TARGETS blosc2_openhtj2k LIBRARY DESTINATION blosc2_openhtj2k)
install(TARGETS open_htj2k LIBRARY DESTINATION blosc2_openhtj2k)

# Test program
add_executable(test_j2k test_j2k.c)
target_link_libraries(test_j2k blosc2_openhtj2k blosc2 -lm)
