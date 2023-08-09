import blosc2
import numpy as np
from PIL import Image

import blosc2_openhtj2k


blosc2.register_codec("openhtj2k", 244)

def im2np(im):
    print('Convert image to np.ndarray:')
    array = np.asarray(im)                  # height x width x channel
    print(f'< shape={array.shape}')
    # channel x width x height. copy() fixes "ndarray is not C-contiguous"
    array = np.transpose(array, (2, 1, 0)).copy()
    print(f'> shape={array.shape}')
    print('  OK')
    print()
    return array

def np2bl(array):
    print('Convert np.ndarray to blosc2:')
    blosc2_openhtj2k.set_params_defaults(transformation=1)
    nthreads = 1
    cparams = {
        'codec': 244,
        'nthreads': nthreads,
        'filters': [],
        'splitmode': blosc2.SplitMode.NEVER_SPLIT,
    }
    dparams = {'nthreads': nthreads}
    array = blosc2.asarray(
        array,
        chunks=array.shape,
        blocks=array.shape,
        cparams=cparams,
        dparams=dparams,
    )
    print(f'> dtype={array.dtype}')
    print(f'> shape={array.shape}')
    print(f'> block={array.blocks}')
    print(f'> chunk={array.chunks}')
    print('  OK')
    print()
    return array

def bl2np(array):
    print('Convert blosc2 to np.ndarray:')
    print(f'< shape={array.shape} {type(array)}')
    array = array[:]
    print(f'> shape={array.shape} {type(array)}')
    print('  OK')
    print()
    return array


def np2im(array):
    print('Convert np.ndarray to image:')
    array = np.transpose(array, (2, 1, 0)).copy()  # channel x width x height
    im = Image.fromarray(array)
    return im


#FILENAME = '../input/officeshots.ppm'
FILENAME = '../input/teapot.ppm'

im = Image.open(FILENAME)       # Load image
array = im2np(im)               # Image to numpy array
array = array.astype('uint32')  # The codec expects 4 bytes per color (xx 00 00 00)
array2 = np2bl(array)           # Numpy array to blosc2 array
print(array2.info)
array3 = bl2np(array2)          # Blosc2 array to numpy
array3 = array3.astype('uint8') # Get back 1 byte per color
im = np2im(array3)
im.show()
