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
    cparams = {'codec': 244, 'nthreads': nthreads}
    #cparams = {'codec': blosc2.Codec.ZSTD, 'nthreads': nthreads}
    dparams = {'nthreads': nthreads}
    array = blosc2.asarray(array, chunks=array.shape, blocks=array.shape, cparams=cparams, dparams=dparams)
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
    #array = array[:3, :381, :165]
    print(f'> shape={array.shape} {type(array)}')
    print('  OK')
    print()
    return array


def np2im(array):
    print('Convert np.ndarray to image:')
    array = np.transpose(array, (2, 1, 0)).copy()  # channel x width x height
    im = Image.fromarray(array)
    return im


#FILENAME = 'input/officeshots.ppm'
FILENAME = 'input/teapot.ppm'

im = Image.open(FILENAME)   # load image
array = im2np(im)           # image to numpy array
array2 = np2bl(array)       # numpy array to blosc2 array
print(array2.info)
array3 = bl2np(array2)      # blosc2 array to numpy
im = np2im(array3)
im.show()
