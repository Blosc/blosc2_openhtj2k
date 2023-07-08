import blosc2
import numpy as np
from PIL import Image

blosc2.register_codec("openhtj2k", 244)

im = Image.open('input/teapot.ppm')
#im = Image.open('input/officeshots.ppm')

print('Convert image to np.ndarray:')
array = np.asarray(im)                  # height x width x channel
print(f'  shape={array.shape}')
array = np.transpose(array, (2, 1, 0))  # channel x width x height
array = np.ascontiguousarray(array)     # fixes "ndarray is not C-contiguous"
print(f'  shape={array.shape}')
print('OK')


nthreads = 1
cparams = {'codec': 244, 'nthreads': nthreads}
dparams = {'nthreads': nthreads}

# FIXME segfault
print('blosc2.asarray(...)')
array = blosc2.asarray(array, cparams=cparams, dparams=dparams)
print('OK')
