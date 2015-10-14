import glob
import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
image = None
for filename in glob.glob('npy/*.npy'):
    data = np.load(filename)
    if image is None:
        image = ax.imshow(data, cmap=plt.cm.Blues, origin='lower')
    else:
        image.set_data(data)
    fig.savefig(filename.replace('npy', 'png'))
