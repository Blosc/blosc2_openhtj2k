# Blosc - Blocked Shuffling and Compression Library
#
# Copyright (C) 2023  The Blosc Developers <blosc@blosc.org>
# https://blosc.org
# License: BSD 3-Clause (see LICENSE.txt)
#
# See LICENSE.txt for details about copyright and rights to use.

cmake_minimum_required(VERSION 3.20)
project(blosc2_openhtj2k LANGUAGES C CXX)
set(CMAKE_CXX_STANDARD 20)

# Needed when working with cibuildwheel and MacOS
set(CMAKE_OSX_DEPLOYMENT_TARGET 10.15)

# Debug build
set(CMAKE_C_FLAGS_DEBUG_INIT "-O0 -g")
set(CMAKE_CXX_FLAGS_DEBUG_INIT "-O0 -g")

message("Building Blosc2 plugin openhtj2k...")

# Find blosc2.h
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
message(STATUS "Executable: ${Python_EXECUTABLE}")

if (UNIX)
    cmake_path(SET Python_LIB NORMALIZE "${Python_STDLIB}/..")
else()
    cmake_path(SET Python_LIB NORMALIZE "${Python_STDLIB}")
endif()

cmake_path(SET Python_ROOT NORMALIZE "${Python_LIB}/..")
message(STATUS "Inferred Python root: ${Python_ROOT}")
cmake_path(SET Python_LIB64 NORMALIZE "${Python_ROOT}/lib64")

cmake_path(SET Python_INCLUDE NORMALIZE "${Python_ROOT}/include")
message(STATUS "Found Python include: ${Python_INCLUDE}")
message(STATUS "Inferred Python lib: ${Python_LIB}")
message(STATUS "Inferred Python lib64: ${Python_LIB64}")

cmake_path(SET Python_Blosc2_INCLUDE NORMALIZE "${Python_ROOT}/include/blosc2.h")
cmake_path(HAS_FILENAME Python_Blosc2_INCLUDE HAS_BLOSC2)
if(HAS_BLOSC2)
    set(BLOSC2_INCLUDE_DIR ${Python_INCLUDE})
    message(STATUS "Found Blosc2 include: ${Python_Blosc2_INCLUDE}")
else()
    message(FATAL_ERROR "No Blosc2 includes found.  Aborting.")
endif()

include_directories("${BLOSC2_INCLUDE_DIR}")
add_subdirectory(src)
