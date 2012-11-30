#! /bin/bash

mdlvis.py -C sim64_cal -s srcA,srcB,srcC,srcD,srcE,srcF,srcG -n 10 --nchan 4 --sfreq=.137 --sdf=.0001 --inttime=10 --startjd=2456234.22 --endjd=2456234.221 --pol=xx 
mk_img.py -C sim64_cal -s zen -p xx new.uv --no_w --size=400 --res=2.
