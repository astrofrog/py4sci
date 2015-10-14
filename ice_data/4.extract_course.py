import os
import glob

import numpy as np

for filename in glob.glob('npy/*01.npy') + glob.glob('npy/*15.npy'):

    data = np.load(filename)

    nan = np.isnan(data)
    data[nan] = 0.
    data = (data[::2, ::2] + data[1::2, ::2] + data[::2, 1::2] + data[1::2, 1::2]) / 4.
    reset = nan[::2, ::2] & nan[1::2, ::2] & nan[::2, 1::2] & nan[1::2, 1::2]
    data[reset] = np.nan

    np.save(filename.replace('npy/', 'npy_course/'), data)

area = np.load('grid/pixel_areas_subset.npy')
area = (area[::2, ::2] + area[1::2, ::2] + area[::2, 1::2] + area[1::2, 1::2]) / 4.
np.save('grid/pixel_areas_subset_down.npy', area)