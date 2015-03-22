#!/bin/bash

python setup.py clear

ln -s 1.mon py4sci_mon
tar czvhf www/_static/py4sci_mon.tgz py4sci_mon
zip -r9 www/_static/py4sci_mon.zip py4sci_mon
rm py4sci_mon

ln -s 1.mon py4sci_tue
tar czvhf www/_static/py4sci_tue.tgz py4sci_tue
zip -r9 www/_static/py4sci_tue.zip py4sci_tue
rm py4sci_tue

ln -s 1.mon py4sci_wed
tar czvhf www/_static/py4sci_wed.tgz py4sci_wed
zip -r9 www/_static/py4sci_wed.zip py4sci_wed
rm py4sci_wed

ln -s 1.mon py4sci_thu
tar czvhf www/_static/py4sci_thu.tgz py4sci_thu
zip -r9 www/_static/py4sci_thu.zip py4sci_thu
rm py4sci_thu

ln -s 1.mon py4sci_fri
tar czvhf www/_static/py4sci_fri.tgz py4sci_fri
zip -r9 www/_static/py4sci_fri.zip py4sci_fri
rm py4sci_fri
