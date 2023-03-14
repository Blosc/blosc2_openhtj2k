add_subdirectory(OpenHTJ2K)
message("dp add subdirectory")

add_library(blosc2_openhtj2k SHARED blosc2_htj2k.cpp)
message("dp add library")

include_directories(OpenHTJ2K/source/core/interface OpenHTJ2K/source/apps/decoder
                OpenHTJ2K/source/core/common OpenHTJ2K/source/core/codestream
                OpenHTJ2K/source/core/coding OpenHTJ2K/source/core/jph
                OpenHTJ2K/source/core/transform)

if(MSVC OR MINGW)
    # Necessary for compiling blosc2_openhtj2k.lib
    set_property(TARGET blosc2_openhtj2k PROPERTY WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()
target_link_libraries(blosc2_openhtj2k open_htj2k)

install(TARGETS blosc2_openhtj2k LIBRARY DESTINATION blosc2_openhtj2k)
