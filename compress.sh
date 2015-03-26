#!/bin/bash

python setup.py clear

ln -s 1.mon py4sci_mon
tar czvhf www/_static/py4sci_mon.tgz --exclude="*Solution*" py4sci_mon
zip -r9 www/_static/py4sci_mon.zip --exclude="*Solution*" py4sci_mon
rm py4sci_mon

ln -s 2.tue py4sci_tue
tar czvhf www/_static/py4sci_tue.tgz --exclude="*Solution*"  py4sci_tue
zip -r9 www/_static/py4sci_tue.zip --exclude="*Solution*" py4sci_tue
rm py4sci_tue

ln -s 3.wed py4sci_wed
tar czvhf www/_static/py4sci_wed.tgz --exclude="*Solution*" --exclude="*ice_data*"  py4sci_wed
zip -r9 www/_static/py4sci_wed.zip --exclude="*Solution*" --exclude="*ice_data*" py4sci_wed
rm py4sci_wed

ln -s 4.thu py4sci_thu
tar czvhf www/_static/py4sci_thu.tgz --exclude="*Solution*"  py4sci_thu
zip -r9 www/_static/py4sci_thu.zip --exclude="*Solution*" py4sci_thu
rm py4sci_thu

# ln -s 5.fri py4sci_fri
# tar czvhf www/_static/py4sci_fri.tgz --exclude="*Solution*"  py4sci_fri
# zip -r9 www/_static/py4sci_fri.zip --exclude="*Solution*" py4sci_fri
# rm py4sci_fri
