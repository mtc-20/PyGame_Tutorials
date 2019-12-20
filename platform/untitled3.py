#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 13:59:49 2019

@author: mtc-20
"""

import time

ctr = 1
prev = time.time()
try:
    while True:
        if time.time() - prev == .5:
            ctr += ctr*(time.time() - prev)
            prev = time.time()
            print("%.3f" % ctr)
#            time.sleep(.1)
            
#        ctr += 1

except KeyboardInterrupt:
    print("Exit")