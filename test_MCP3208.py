#!/usr/bin/python
from MCP3208 import MCP3208, MCP3208Error
import RPi.GPIO as GPIO

import time


if __name__ == '__main__':
    cs_pin = 31
    clock_pin = 23
    data_out_pin = 19
    data_in_pin = 21
    MCP3208_ADC = MCP3208(cs_pin, clock_pin, data_in_pin, data_out_pin, GPIO.BOARD)
    running = True
    while(running):
        try:
            for channel in range (0,9):
                try:
                    measurement = str(MCP3208_ADC.get(channel))
                except MCP3208Error as e:
                    measurement = "Error: "+ e.value
                print("Measured value (ch%d): " % (channel) + measurement)
            print("")
            time.sleep(1)
        except KeyboardInterrupt:
            running = False
    MCP3208_ADC.cleanup()
