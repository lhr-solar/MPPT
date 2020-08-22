"""
ni_cell_data.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 7/10/20
Last Modified: 8/22/20
Description: Parses, cleans, and displays cell data collected from the EER Labview test setup.
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv


# 1 light
f = open("Cell_Measurements_7_10_20/1Light_data_7_10_20.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages1 = []
currents1 = []
powers1 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip('\n').split('\t')[1::][1])
        current = float(line.strip('\n').split('\t')[1::][0])*200
        voltages1.append(voltage)
        currents1.append(current)
        powers1.append(voltage*current)
    except Exception:
        pass


# 2 lights
f = open("Cell_Measurements_7_10_20/2Lights_data_7_10_20.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages2 = []
currents2 = []
powers2 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip('\n').split('\t')[1::][1])
        current = float(line.strip('\n').split('\t')[1::][0])*200
        voltages2.append(voltage)
        currents2.append(current)
        powers2.append(voltage*current)
    except Exception:
        pass


# 3 lights
f = open("Cell_Measurements_7_10_20/3Lights_data_7_10_20.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages3 = []
currents3 = []
powers3 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip('\n').split('\t')[1::][1])
        current = float(line.strip('\n').split('\t')[1::][0])*200
        voltages3.append(voltage)
        currents3.append(current)
        powers3.append(voltage*current)
    except Exception:
        pass


fig, ax = plt.subplots(2, 1)
fig.set_size_inches(9, 10)

ax[0].set_xlabel('Cell Voltage (V)')
ax[0].set_ylabel('Cell Current (A)')
ax[0].set_xlim([0, .7])
ax[0].set_ylim([0, 5])
ax[0].scatter(voltages1, currents1, color='r', marker='o', s=[1])
ax[0].scatter(voltages2, currents2, color='g', marker='v', s=[1])
ax[0].scatter(voltages3, currents3, color='b', marker='D', s=[1])
ax[0].legend(labels=('1 Light', '2 Lights', '3 Lights'), loc="upper left")
ax[0].title.set_text("Cell current as a function of voltage")

ax[0].grid()

ax[1].set_xlabel('Cell Voltage (V)')
ax[1].set_ylabel('Cell Power (W)')
ax[1].set_xlim([0, .7])
ax[1].set_ylim([0, 2])
ax[1].scatter(voltages1, powers1, color='r', marker='o', s=[1])
ax[1].scatter(voltages2, powers2, color='g', marker='v', s=[1])
ax[1].scatter(voltages3, powers3, color='b', marker='D', s=[1])
ax[1].legend(labels=('1 Light', '2 Lights', '3 Lights'), loc="upper left")
ax[1].title.set_text("Cell power as a function of voltage")
ax[1].grid()

plt.tight_layout()

fig.savefig("test.png")
plt.show()

# save into a file
with open("model.csv", "w", newline='\n') as csv_file:
    writer = csv.writer(csv_file)
    for idx in range(len(voltages1)):
        writer.writerow([voltages1[idx], currents1[idx], 255, 0, 0])
        writer.writerow([voltages2[idx], currents2[idx], 0, 255, 0])
        writer.writerow([voltages3[idx], currents3[idx], 0, 0, 255])