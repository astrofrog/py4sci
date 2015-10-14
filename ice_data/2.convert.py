import os
import glob

for filename_gz in glob.glob('raw/asi-*.hdf.gz'):
    print("Converting", filename_gz)
    os.system('gunzip ' + filename_gz)
    filename = filename_gz.replace('.gz', '')
    filename_out = filename.replace('raw', 'hdf5').replace('.hdf', '.h5')
    filename_out = filename_out.replace('asi-n6250-', '')
    filename_out = filename_out.replace('-v5', '')
    os.system('h4toh5 {0} {1}'.format(filename, filename_out))
