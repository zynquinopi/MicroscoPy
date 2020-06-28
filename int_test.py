#!/usr/bin/python
# -*- coding: utf-8 -*-

import pigpio
import time 
import math

pi = pigpio.pi()
pi.set_mode(17, pigpio.INPUT)
pi.set_pull_up_down(17, pigpio.PUD_UP)
pi.set_mode(4, pigpio.OUTPUT)

i2c_device = pi.i2c_open(1, 0x20)

# MCP23017 setup portA
pi.i2c_write_device(i2c_device, [0x00, 0x00])  #output
# pi.i2c_write_device(i2c_device, [0x, 0x])  #pullup
# pi.i2c_write_device(i2c_device, [0x, 0x])  #inten

# MCP23017 setup portB
pi.i2c_write_device(i2c_device, [0x01, 0xFF])  #input
pi.i2c_write_device(i2c_device, [0x0D, 0xFF])  #pullup
pi.i2c_write_device(i2c_device, [0x05, 0xFF])  #inten


def cb_interrupt(gpio, level, tick):
    # print (gpio, level, tick)
    pi.write(4, 1)

    _, intpin = pi.i2c_read_i2c_block_data(i2c_device, 0x0F, 1)
    _, pinval = pi.i2c_read_i2c_block_data(i2c_device, 0x13, 1)
    val = (intpin[0] & pinval[0]) >> int(math.log2(intpin[0]))
    # time.sleep(1)
    pi.write(4, 0)


cb = pi.callback(17, pigpio.FALLING_EDGE, cb_interrupt)

while(True):
    pass