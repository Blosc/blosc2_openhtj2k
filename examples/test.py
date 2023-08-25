import argparse

import blosc2
import blosc2_openhtj2k
import numpy as np
from PIL import Image


# Register the codec, with this number we will tell blosc2 to use the openhj2k codec.
# This is done once.
blosc2.register_codec("openhtj2k", 244)

def compress(im):
    """This function gets a PIL image and returns a blosc2 array.
    """
    # Convert the image to a numpy array, it will have 3 dimensions: height, width, color.
    np_array = np.asarray(im)

    # Transpose the array so the is shape as expected by the plugin, with the color first.
    # The call to copy() makes the array C-contiguous, as required by the plugin.
    np_array = np.transpose(np_array, (2, 1, 0)).copy()

    # The library expects 4 bytes per color (xx 00 00 00), so change the type.
    np_array = np_array.astype('uint32')

    # Set the parameters that will be used by the codec
    blosc2_openhtj2k.set_params_defaults(transformation=1)

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
    )

    # Print information about the array, see the compression ratio (cratio)
    print(bl_array.info)

    return bl_array


def decompress(bl_array):
    """This function gets a blosc2 array and returns a PIL image.
    """
    # Transform the blosc2 array to a numpy array. This is where decompression happens.
    np_array = bl_array[:]

    # Get back 1 byte per color (the codec works with uint32)
    np_array = np_array.astype('uint8')

    # Get back the original shape: height, width, channel
    np_array = np.transpose(np_array, (2, 1, 0))

    # Transfom the numpy array to a PIL image
    im = Image.fromarray(np_array)

    return im


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compress and decompress the given input image',
    )
    parser.add_argument('inputfile')
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    # Load the image using PIL
    im = Image.open(args.inputfile)
    bl_array = compress(im)
    im = decompress(bl_array)

    if args.show:
        im.show()
