import argparse

import blosc2
import numpy as np
from PIL import Image


# Register the codec, with this number we will tell blosc2 to use the openhj2k codec.
# This is done once.
blosc2.register_codec("openhtj2k", 244)

def decompress(array):
    """This function gets a blosc2 array and returns a PIL image.
    """
    # Transform the blosc2 array to a numpy array. This is where decompression happens.
    np_array = array[:]

    # Get back 1 byte per color, change dtype from uint32 to uint8
    np_array = np_array.astype('uint8')

    # Get back the original shape: height, width, channel
    np_array = np.transpose(np_array, (2, 1, 0))

    # Transfom the numpy array to a PIL image
    im = Image.fromarray(np_array)

    return im


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Decompress the given Blosc2 file, and optionally display the image',
    )
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    array = blosc2.open(args.inputfile)
    im = decompress(array)
    im.save(args.outputfile)

    if args.show:
        im.show()
