#! /usr/bin/env python3
import ftplib
import os
import sys
from datetime import datetime

import requests

import matplotlib.pyplot as plt


address = 1
pin_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
ref_voltage = 3.3
divider = 5.7 # see https://www.enigma14.eu/wiki/AD_Converter_PCF8591_for_Raspberry_Pi


if __name__ == '__main__':
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    charge = ""

    filename = "data_{}.txt".format(datetime.now().strftime("%m"))

    # if last modification date of the file was one year before, empty file
    if os.path.isfile(filename):
        stat = os.stat(filename)

        if datetime.fromtimestamp(stat.st_mtime).strftime("%m") < datetime.now().strftime("%m"):
            open(filename, 'w').close()

    # Get current Value
    result = requests.get("http://192.168.1.25/")

    value = result.text
    print("read: {}".format(value))

    num = float(value)
    if num < 11.6:
        charge = "0%"
    elif num < 12.0:
        charge = "30%"
    elif num < 12.2:
        charge = "50%"
    elif num < 12.5:
        charge = "75%"
    else:
        charge = "100%"

    with open(filename, "a") as myfile:
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

    ax.set(xlabel="{} - {} - {}V".format(date, charge, value), ylabel='voltage (V)')
    ax.grid()

    fig.savefig("battery.png")

    # upload to FTP
    session = ftplib.FTP(os.environ['URL'], os.environ['USERNAME'], os.environ['PASSWORD'])
    file = open('battery.png', 'rb')
    session.storbinary('STOR battery.png', file)
    file.close()
    session.quit()
