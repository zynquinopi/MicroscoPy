#!/usr/bin/env python
# channel 0 pin1-GND
import spidev
Vref = 3.29476
 
spi = spidev.SpiDev()
spi.open(0,0) #port 0,cs 0
spi.max_speed_hz = 1000000
 
while True:
    adc = spi.xfer2([0x01,0x80,0x00])
    data = ((adc[1] & 3) << 8) | adc[2]
    print (str(Vref*data/1024) + "V")
 
spi.close()