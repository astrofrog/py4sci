import h5py
import numpy as np

def vincenty_sphere_dist(lon1, lat1, lon2, lat2):

    from numpy import arctan2, sin, cos

    sdlon = sin(lon2 - lon1)
    cdlon = cos(lon2 - lon1)
    slat1 = sin(lat1)
    slat2 = sin(lat2)
    clat1 = cos(lat1)
    clat2 = cos(lat2)

    num1 = clat2 * sdlon
    num2 = clat1 * slat2 - slat1 * clat2 * cdlon
    denominator = slat1 * slat2 + clat1 * clat2 * cdlon

    return arctan2((num1 ** 2 + num2 ** 2) ** 0.5, denominator)

f = h5py.File('grid/LongitudeLatitudeGrid-n6250-Arctic.h5')
lon = np.radians(np.array(f['Longitudes']))
lat = np.radians(np.array(f['Latitudes']))

dx = vincenty_sphere_dist(lon[2:, 1:-1], lat[2:, 1:-1], lon[:-2, 1:-1], lat[:-2, 1:-1])
dy = vincenty_sphere_dist(lon[1:-1, 2:], lat[1:-1, 2:], lon[1:-1, :-2], lat[1:-1, :-2])

area = np.zeros(lon.shape)
area[1:-1, 1:-1] = dx * dy * 6371. ** 2
area[0,:] = area[1,:]
area[-1,:] = area[-2,:]
area[:, 0] = area[:,1]
area[:,-1] = area[:,-2]

np.save('grid/pixel_areas.npy', area)
np.save('grid/pixel_areas_subset.npy', area[300:1400,100:1100])

print(np.sum(area) / (6371 ** 2 * 4 * np.pi))