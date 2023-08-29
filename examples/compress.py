import argparse
from pathlib import Path

import blosc2
import blosc2_openhtj2k
import numpy as np
from PIL import Image


# Register the codec, with this number we will tell blosc2 to use the openhj2k codec.
# This is done once.
blosc2.register_codec("openhtj2k", 244)

def compress(im, urlpath=None, **kwargs):
    """
    This function gets a PIL image and returns a Blosc2 array.

    If the optional argument urlpath is given, the Blosc2 array will be saved to that
    location.

    Other keyword arguments are passed to blosc2_openhtj2k.set_params_defaults(...)
    """
    # Convert the image to a numpy array
    np_array = np.asarray(im)

    # Transpose the array so the channel (color) comes first
    # Change from (height, width, channel) to (channel, width, height)
    np_array = np.transpose(np_array, (2, 1, 0))

    # Make the array C-contiguous
    np_array = np_array.copy()

    # The library expects 4 bytes per color (xx 00 00 00), so change the type
    np_array = np_array.astype('uint32')

    # Set the parameters that will be used by the codec
    blosc2_openhtj2k.set_params_defaults(**kwargs)

    # Multithreading is not supported, so we must set the number of threads to 1
    nthreads = 1

    # Define the compression and decompression paramaters. Disable the filters and the
    # splitmode, because these don't work with the codec.
    cparams = {
        'codec': 244,
        'nthreads': nthreads,
        'filters': [],
        'splitmode': blosc2.SplitMode.NEVER_SPLIT,
    }
    dparams = {'nthreads': nthreads}

    # Transform the numpy array to a blosc2 array. This is where compression happens, and
    # the HTJ2K codec is called.
    bl_array = blosc2.asarray(
        np_array,
        chunks=np_array.shape,
        blocks=np_array.shape,
        cparams=cparams,
        dparams=dparams,
        urlpath=urlpath,
    )

    # Print information about the array, see the compression ratio (cratio)
    print(bl_array.info)

    return bl_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compress the given input image using Blosc2 and OpenHTJ2K',
    )
    add_argument = parser.add_argument
    add_argument('inputfile')
    add_argument('outputfile')
    add_argument('--transformation', type=int, help='0:lossy 1:lossless (default is 1)')
    add_argument('--qfactor', type=int, help='Quality factor: 0-100')
    #add_argument('--isJPH', action='store_true', help='')
    add_argument('--color-space', type=int, help='0:RGB 1:YCC')
    add_argument('--blkwidth', type=int, help='Precinct width (default: 4)')
    add_argument('--blkheight', type=int, help='Precinct height (default: 4)')
    args = parser.parse_args()

    kwargs = {
        k: v for k, v in args._get_kwargs()
        if k in blosc2_openhtj2k.params_defaults and v is not None
    }

    im = Image.open(args.inputfile)
    Path(args.outputfile).unlink(missing_ok=True)
    compress(im, args.outputfile, **kwargs)
