#!/bin/bash

export OMP_NUM_THREADS=1

source /home/pi/yolo-env/bin/activate

cd /home/pi/hklpr_yolov5_pi

python3 testpower.py