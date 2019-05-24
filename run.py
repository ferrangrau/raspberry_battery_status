#! /usr/bin/env python3

import sys
from datetime import datetime
from quick2wire.parts.pcf8591 import *
from quick2wire.i2c import I2CMaster

import matplotlib.pyplot as plt
import numpy as np


address = 1
pin_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
ref_voltage = 3.3
divider = 5.7 # see https://www.enigma14.eu/wiki/AD_Converter_PCF8591_for_Raspberry_Pi


if __name__ == '__main__':
    # Get new Value
    with I2CMaster() as i2c:
        adc = PCF8591(i2c, FOUR_SINGLE_ENDED)
        pin = adc.single_ended_input(pin_index)

        value = ref_voltage*divider*pin.value
        print("read: {}".format(value))
        with open("data.txt", "a") as myfile:
            myfile.write("{}, {}\n".format(datetime.now().strftime("%Y%m%d%H%M%S"), value))

    # Data for plotting
    t = []
    s = []
    with open('data.txt') as fp:
        for cnt, line in enumerate(fp):
            data = line.split(",")
            t.append(int(data[0].strip()))
            s.append(float(data[1].strip()))

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time', ylabel='voltage (V)')
    ax.xticks(np.arange(min(t), max(t)+1, 1.0))
    ax.grid()

    fig.savefig("battery.png")
