#! /bin/bash

mdlvis.py -C sim64w_cal -s srcA,srcB,srcC,srcD,srcE,srcF,srcG,srcH,srcI,srcJ,srcK,srcL -n 10 --nchan 4 --sfreq=.137 --sdf=.00001 --inttime=100 --startjd=2456234.22 --endjd=2456234.221 --pol=xx
mk_img.py -C sim64w_cal -s zen -p xx new.uv --no_w --size=400 --res=.5 --cnt=10
mk_img.py -C sim64w_cal -s zen -p xx new.uv --size=400 --res=.5 --cnt=11
