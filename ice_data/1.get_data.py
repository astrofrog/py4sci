import os
from urllib.request import urlopen

URL = "http://www.iup.uni-bremen.de/seaice/amsredata/asi_daygrid_swath/l1a/n6250/{year}/{month}/asi{prefix}-n6250-{year}{month_num:02d}{day:02d}-v5.hdf{suffix}"

MONTHS = {}
MONTHS[1] = 'jan'
MONTHS[2] = 'feb'
MONTHS[3] = 'mar'
MONTHS[4] = 'apr'
MONTHS[5] = 'may'
MONTHS[6] = 'jun'
MONTHS[7] = 'jul'
MONTHS[8] = 'aug'
MONTHS[9] = 'sep'
MONTHS[10] = 'oct'
MONTHS[11] = 'nov'
MONTHS[12] = 'dec'

dates = []
for suffix in ['', '.gz'][1:]:
    for prefix in ['', '180']:
        for year in range(2006, 2013):
            for month in range(1, 13):
                for day in range(1, 32):
                    dates.append((prefix, year, month, day, suffix))


def download(date):    
    prefix, year, month, day, suffix = date    
    filename = 'raw/asi{prefix}-n6250-{year}{month_num:02d}{day:02d}-v5.hdf{suffix}'.format(prefix=prefix, year=year, month_num=month, day=day, suffix=suffix)
    if os.path.exists(filename):
        return
    print("Downloading", filename)
    try:
        u = urlopen(URL.format(prefix=prefix, year=year, month_num=month, month=MONTHS[month], day=day, suffix=suffix))
        content = u.read()
    except:
        return
    if b'DOCTYPE' in content:
        return
    open(filename, 'wb').write(content)

import multiprocessing as mp
p = mp.Pool(processes=8)
p.map(download, dates)
