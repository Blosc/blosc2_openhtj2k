add_subdirectory(OpenHTJ2K)
add_library(blosc2_openhtj2k MODULE blosc2_htj2k.cpp)

include_directories(OpenHTJ2K/source/core/interface OpenHTJ2K/source/apps/decoder
                OpenHTJ2K/source/core/common OpenHTJ2K/source/core/codestream
                OpenHTJ2K/source/core/coding OpenHTJ2K/source/core/jph
                OpenHTJ2K/source/core/transform)

if(MSVC OR MINGW)
    # Necessary for compiling blosc2_openhtj2k.lib
    set_property(TARGET blosc2_openhtj2k PROPERTY WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()
target_link_libraries(blosc2_openhtj2k open_htj2k)


link_directories(${Python_LIB})
include_directories(${Python_INCLUDE})

add_executable(test_j2k "test_j2k.c")
target_link_libraries(test_j2k -lm blosc2)


# This is needed for finding sibling libraries in the same directory for MacOS and Linux
# TODO: Figure out how to do that in Windows
if(APPLE)
    set_target_properties(blosc2_openhtj2k PROPERTIES INSTALL_RPATH "@loader_path/.")
elseif(UNIX)
    set_target_properties(blosc2_openhtj2k PROPERTIES INSTALL_RPATH "\${ORIGIN}/.")
endif()

install(TARGETS blosc2_openhtj2k LIBRARY DESTINATION blosc2_openhtj2k)
install(TARGETS open_htj2k LIBRARY DESTINATION blosc2_openhtj2k)
