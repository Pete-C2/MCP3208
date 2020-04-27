# MCP3208
Python driver for [MCP3208 12-bit Analog-to-Digital Converter](http://www.microchip.com/downloads/en/DeviceDoc/21298e.pdf)

Requires:
- The [GPIO Library](https://sourceforge.net/projects/raspberry-gpio-python/) (Already on most Raspberry Pi OS builds)
- A [Raspberry Pi](http://www.raspberrypi.org/)

## Basic use

```python

#!/usr/bin/python
from MCP3208 import MCP3208, MCP3208Error

cs_pin = 31
clock_pin = 23
data_out_pin = 19
data_in_pin = 21
channel = 0
MCP3208_ADC = MCP3208(cs_pin, clock_pin, data_in_pin, data_out_pin, GPIO.BOARD)
print(MCP3208_ADC.get(channel))
thermocouple.cleanup()

```

*Note: these are the GPIO header pin numbers, not the GPIO pin numbers.*  
*This can be modified by passing `GPIO.BCM` as the fifth [init parameter](https://github.com/Pete-C2/MCP3208/blob/master/MCP3208.py#L11).*

See test_MCP3208.py for a test example.

## Changelog

### V0.2

- Amended test code to measure every channel and check handling of attempting to measure an invalid channel

### V0.1

- Initial code.
