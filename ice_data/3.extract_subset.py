import glob

import h5py
import numpy as np

for filename in glob.glob('hdf5/*.h5'):

    f = h5py.File(filename)
    data = np.array(f['ASI Ice Concentration'])
    subset = data[300:1400,100:1100]

    # Fix poles
    pole = subset[500:600,465:565]
    pole[np.isnan(pole)] = 100.
    np.save(filename.replace('hdf5', 'npy').replace('h5', 'npy'), subset)
    f.close()
