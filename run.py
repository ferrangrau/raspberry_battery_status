#! /usr/bin/env python3
import ftplib
import os
import sys
from datetime import datetime
from quick2wire.parts.pcf8591 import *
from quick2wire.i2c import I2CMaster

import matplotlib.pyplot as plt


address = 1
pin_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
ref_voltage = 3.3
divider = 5.7 # see https://www.enigma14.eu/wiki/AD_Converter_PCF8591_for_Raspberry_Pi


if __name__ == '__main__':
    date: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    charge: str = ""

    """
    Batería al 100% (totalmente cargada) = 12,7 V (voltios)
    Batería al 75% = 12,5 V
    Batería al 50% = 12,2 V
    Batería al 30% = 12 V
    Batería descargada = 11,6 V
    """
    # Get new Value
    with I2CMaster() as i2c:
        adc = PCF8591(i2c, FOUR_SINGLE_ENDED)
        pin = adc.single_ended_input(pin_index)

        value = ref_voltage*divider*pin.value
        print("read: {}".format(value))

        if value < 11.6:
            charge = "0%"
        elif value < 12.0:
            charge = "30%"
        elif value < 12.2:
            charge = "50%"
        elif charge < 12.5:
            value = "75%"
        else:
            charge = "100%"

        with open("data.txt", "a") as myfile:
            myfile.write("{}, {}\n".format(date, value))

    # Data for plotting
    t = []
    s = []
    with open('data.txt') as fp:
        for cnt, line in enumerate(fp):
            data = line.split(",")
            t.append(cnt)
            s.append(float(data[1].strip()))

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel="{} - {}".format(date, charge), ylabel='voltage (V)')
    ax.grid()

    fig.savefig("battery.png")

    # upload to FTP
    session = ftplib.FTP(os.environ['URL'], os.environ['USERNAME'], os.environ['PASSWORD'])
    file = open('battery.png', 'rb')
    session.storbinary('STOR battery.png', file)
    file.close()
    session.quit()
