import argparse
from pathlib import Path

import blosc2
import blosc2_openhtj2k
import numpy as np
from PIL import Image


# Register the codec, with this number we will tell blosc2 to use the openhj2k codec.
# This is done once.
blosc2.register_codec("openhtj2k", 244)

def compress(im, urlpath=None):
    """This function gets a PIL image and returns a blosc2 array.
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
    blosc2_openhtj2k.set_params_defaults(
        transformation=0,   # 0:lossy 1:lossless (default is 1)
    )

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
    print('XXX', np_array.shape) # 3, 256, 256
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
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    args = parser.parse_args()

    im = Image.open(args.inputfile)
    Path(args.outputfile).unlink(missing_ok=True)
    compress(im, args.outputfile)
