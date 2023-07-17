# Blosc - Blocked Shuffling and Compression Library
#
# Copyright (C) 2023  The Blosc Developers <blosc@blosc.org>
# https://blosc.org
# License: BSD 3-Clause (see LICENSE.txt)
#
# See LICENSE.txt for details about copyright and rights to use.

VERSION = 0.1

import ctypes
import os
import platform
from pathlib import Path


def get_libpath():
    system = platform.system()
    if system in ["Linux", "Darwin"]:
        libname = "libblosc2_openhtj2k.so"
    elif system == "Windows":
        libname = "libblosc2_openhtj2k.dll"
    else:
        raise RuntimeError("Unsupported system: ", system)
    return os.path.abspath(Path(__file__).parent / libname)

def print_libpath():
    libpath = get_libpath()
    print(libpath, end="")


params_defaults = {
    'qfactor'               : 255,
    'isJPH'                 : False,
    'color_space'           : 0,
    # COD
    'blkwidth'              : 4,
    'blkheight'             : 4,
    'is_max_precincts'      : True,
    'use_SOP'               : False,
    'use_EPH'               : False,
    'progression_order'     : 0,
    'number_of_layers'      : 1,
    'use_color_trafo'       : 1,
    'dwt_levels'            : 5,
    'codeblock_style'       : 0x040,
    'transformation'        : 1,
    # QCD
    'number_of_guardbits'   : 1,
    'is_derived'            : False,
    'base_step'             : 0.0,
}

def set_params_defaults(**kwargs):
    # Check arguments
    not_supported = [k for k in kwargs.keys() if k not in params_defaults]
    if not_supported != []:
        raise ValueError(f"The next params are not supported: {not_supported}")

    # Prepare arguments
    params = params_defaults.copy()
    params.update(kwargs)
    args = params.values()
    args = list(args)
    args[16] = ctypes.c_double(args[16])

    libpath = get_libpath()
    lib = ctypes.cdll.LoadLibrary(libpath)
    lib.set_params_defaults(*args)


if __name__ == "__main__":
    print_libpath()
