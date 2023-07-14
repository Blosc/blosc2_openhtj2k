# Blosc - Blocked Shuffling and Compression Library
#
# Copyright (C) 2023  The Blosc Developers <blosc@blosc.org>
# https://blosc.org
# License: BSD 3-Clause (see LICENSE.txt)
#
# See LICENSE.txt for details about copyright and rights to use.

VERSION = 0.1

from ctypes import cdll
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


def set_params_default(qfactor):
    libpath = get_libpath()
    lib = cdll.LoadLibrary(libpath)
    lib.set_params_default(qfactor)


if __name__ == "__main__":
    print_libpath()
