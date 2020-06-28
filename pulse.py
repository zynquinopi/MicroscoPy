#!/usr/bin/python
# -*- coding: utf-8 -*-

import pigpio
import time 

pi = pigpio.pi()
pi.set_mode(27, pigpio.OUTPUT)



while(True):
    pi.write(27, 1)
    time.sleep(0.04)
    pi.write(27, 0)
    time.sleep(0.04)