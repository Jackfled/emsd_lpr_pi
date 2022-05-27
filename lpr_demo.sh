#!/bin/bash

export OMP_NUM_THREADS=1

source /home/pi/yolo-env/bin/activate

cd /home/pi/hklpr_yolov5

python3 lp_detect_recog.py