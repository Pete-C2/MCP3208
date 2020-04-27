#!/usr/bin/python
import RPi.GPIO as GPIO

class MCP3208(object):
    '''Python driver for [MCP3208 12-bit Analog-to-Digital Converter](http://www.microchip.com/downloads/en/DeviceDoc/21298e.pdf)
     Requires:
     - The [GPIO Library](https://code.google.com/p/raspberry-gpio-python/) (Already on most Raspberry Pi OS builds)
     - A [Raspberry Pi](http://www.raspberrypi.org/)

    '''
    def __init__(self, cs_pin, clock_pin, data_in_pin, data_out_pin, board = GPIO.BCM):
        '''Initialize Soft (Bitbang) SPI bus

        Parameters:
        - cs_pin:    Chip Select (CS) / Slave Select (SS) pin (Any GPIO)  
        - clock_pin: Clock (CLK / SCK) pin (Any GPIO)
        - data_in_pin:  Data input (to RPi) (DOUT(MCP3208) / MISO) pin (Any GPIO)
        - data_out_pin:  Data output (from RPi) (DIN(MCP3208) / MOSI) pin (Any GPIO)
        - board:     (optional) pin numbering method as per RPi.GPIO library (GPIO.BCM (default) | GPIO.BOARD)

        '''
        self.cs_pin = cs_pin
        self.clock_pin = clock_pin
        self.data_in_pin = data_in_pin
        self.data_out_pin = data_out_pin
        self.data = None
        self.board = board

        # Initialize needed GPIO
        GPIO.setmode(self.board)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.data_in_pin, GPIO.IN)
        GPIO.setup(self.data_out_pin, GPIO.OUT)

        # Pull chip select high to make chip inactive
        GPIO.output(self.cs_pin, GPIO.HIGH)

        # Initialise clock low and data out high
        GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.data_out_pin, GPIO.HIGH)

    def get(self, channel = 0):
        '''Read one value from one channel

        Parameters:
        - channel:    The channel to read, default 0  

        '''
        if channel > 7 or channel < 0:
            raise Exception('MCP3208 channel out of range: ' + str(channel))
        # Ensure data out is high
        GPIO.output(self.data_out_pin, GPIO.HIGH)
        
        # Select the chip
        GPIO.output(self.cs_pin, GPIO.LOW)        

        # Start bit
        GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.data_out_pin, GPIO.HIGH)
        GPIO.output(self.clock_pin, GPIO.HIGH)

        # Define single ended measurement
        GPIO.output(self.clock_pin, GPIO.LOW)
        GPIO.output(self.data_out_pin, GPIO.HIGH)
        GPIO.output(self.clock_pin, GPIO.HIGH)

        # Define the measurement channel
        # D2
        GPIO.output(self.clock_pin, GPIO.LOW)
        if (channel & 4) == 0:
            GPIO.output(self.data_out_pin, GPIO.LOW)
        else:
            GPIO.output(self.data_out_pin, GPIO.HIGH)
        GPIO.output(self.clock_pin, GPIO.HIGH)
        
        # D1
        GPIO.output(self.clock_pin, GPIO.LOW)
        if (channel & 2) == 0:
            GPIO.output(self.data_out_pin, GPIO.LOW)
        else:
            GPIO.output(self.data_out_pin, GPIO.HIGH)
        GPIO.output(self.clock_pin, GPIO.HIGH)
        
        # D0
        GPIO.output(self.clock_pin, GPIO.LOW)
        if (channel & 1) == 0:
            GPIO.output(self.data_out_pin, GPIO.LOW)
        else:
            GPIO.output(self.data_out_pin, GPIO.HIGH)
        GPIO.output(self.clock_pin, GPIO.HIGH)
       
        # Sample and hold period
        GPIO.output(self.clock_pin, GPIO.LOW)

        GPIO.output(self.clock_pin, GPIO.HIGH)
        
        # Null bit
        GPIO.output(self.clock_pin, GPIO.LOW)

        GPIO.output(self.clock_pin, GPIO.HIGH)
        
        bytesin = 0
        # Read in 12 bits
        for i in range(12):
            GPIO.output(self.clock_pin, GPIO.LOW)
            bytesin = bytesin << 1
            if (GPIO.input(self.data_in_pin)):
                bytesin = bytesin | 1
            GPIO.output(self.clock_pin, GPIO.HIGH)
        # Unselect the chip
        GPIO.output(self.cs_pin, GPIO.HIGH)
        # Save data
        return bytesin

    def cleanup(self):
        '''Selective GPIO cleanup'''
        GPIO.setup(self.cs_pin, GPIO.IN)
        GPIO.setup(self.clock_pin, GPIO.IN)
        GPIO.setup(self.data_out_pin, GPIO.IN)

class MCP3208Error(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

