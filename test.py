import blosc2
import numpy as np
from PIL import Image

import blosc2_openhtj2k

blosc2.register_codec("openhtj2k", 244)

def im2np(im):
    print('Convert image to np.ndarray:')
    array = np.asarray(im)                  # height x width x channel
    print(f'  shape={array.shape}')
    array = np.transpose(array, (2, 1, 0))  # channel x width x height
    array = np.ascontiguousarray(array)     # fixes "ndarray is not C-contiguous"
    print(f'  shape={array.shape}')
    print('  OK')
    return array

def np2bl(array):
    print('Convert np.ndarray to blosc2:')
    blosc2_openhtj2k.set_params_defaults(transformation=0)
    nthreads = 1
    cparams = {'codec': 244, 'nthreads': nthreads}
    dparams = {'nthreads': nthreads}
    array = blosc2.asarray(array, cparams=cparams, dparams=dparams)
    print('  OK')
    return array

def np2im(array):
    array = np.transpose(array, (2, 1, 0))  # channel x width x height
    im = Image.fromarray(array)
    return im


FILENAME = 'input/officeshots.ppm'
#FILENAME = 'input/teapot.ppm'

im = Image.open(FILENAME)   # load image
array = im2np(im)           # image to numpy array
array = np2bl(array)        # numpy array to blosc2 array
array = np.asarray(array)   # blosc2 array to numpy array
#im = np2im(array)
#im.show()
