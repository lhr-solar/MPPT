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
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages1.append(voltage)
        currents1.append(current)
        powers1.append(voltage * current)
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
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages2.append(voltage)
        currents2.append(current)
        powers2.append(voltage * current)
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
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages3.append(voltage)
        currents3.append(current)
        powers3.append(voltage * current)
    except Exception:
        pass


# ---
# south light
f = open("Cell_Measurements_9_10_20/1light_south_A.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages4 = []
currents4 = []
powers4 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages4.append(voltage)
        currents4.append(current)
        powers4.append(voltage * current)
    except Exception:
        pass

f = open("Cell_Measurements_9_10_20/1light_south_B.lvm", "r")
for line in range(0, 22):
    f.readline()


while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages4.append(voltage)
        currents4.append(current)
        powers4.append(voltage * current)
    except Exception:
        pass


# north light
f = open("Cell_Measurements_9_10_20/1light_north_A.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages5 = []
currents5 = []
powers5 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages5.append(voltage)
        currents5.append(current)
        powers5.append(voltage * current)
    except Exception:
        pass

f = open("Cell_Measurements_9_10_20/1light_north_B.lvm", "r")
for line in range(0, 22):
    f.readline()

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages5.append(voltage)
        currents5.append(current)
        powers5.append(voltage * current)
    except Exception:
        pass


# center light
f = open("Cell_Measurements_9_10_20/1light_center_A.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages6 = []
currents6 = []
powers6 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages6.append(voltage)
        currents6.append(current)
        powers6.append(voltage * current)
    except Exception:
        pass

f = open("Cell_Measurements_9_10_20/1light_center_B.lvm", "r")
for line in range(0, 22):
    f.readline()

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages6.append(voltage)
        currents6.append(current)
        powers6.append(voltage * current)
    except Exception:
        pass


# south and north light
f = open("Cell_Measurements_9_10_20/2lights_NS_A.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages7 = []
currents7 = []
powers7 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages7.append(voltage)
        currents7.append(current)
        powers7.append(voltage * current)
    except Exception:
        pass

f = open("Cell_Measurements_9_10_20/2lights_NS_B.lvm", "r")
for line in range(0, 22):
    f.readline()

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages7.append(voltage)
        currents7.append(current)
        powers7.append(voltage * current)
    except Exception:
        pass


# all lights
f = open("Cell_Measurements_9_10_20/3lights_A.lvm", "r")
for line in range(0, 22):
    f.readline()

voltages8 = []
currents8 = []
powers8 = []

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages8.append(voltage)
        currents8.append(current)
        powers8.append(voltage * current)
    except Exception:
        pass

f = open("Cell_Measurements_9_10_20/3lights_B.lvm", "r")
for line in range(0, 22):
    f.readline()

while True:
    line = f.readline()
    line = f.readline()
    if not line:
        break
    try:
        voltage = float(line.strip("\n").split("\t")[1::][1])
        current = float(line.strip("\n").split("\t")[1::][0]) * 200
        voltages8.append(voltage)
        currents8.append(current)
        powers8.append(voltage * current)
    except Exception:
        pass


fig, ax = plt.subplots(2, 1)
fig.set_size_inches(9, 10)

ax[0].set_xlabel("Cell Voltage (V)")
ax[0].set_ylabel("Cell Current (A)")
ax[0].set_xlim([0, 0.7])
ax[0].set_ylim([0, 5])
ax[0].scatter(voltages4, currents4, color="r", marker="o", s=[1])
ax[0].scatter(voltages5, currents5, color="g", marker="v", s=[1])
ax[0].scatter(voltages6, currents6, color="b", marker="D", s=[1])
ax[0].scatter(voltages7, currents7, color="y", marker="o", s=[1])
ax[0].scatter(voltages8, currents8, color="k", marker="v", s=[1])
ax[0].legend(
    labels=("S Light", "N Light", "C Light", "NS Lights", "All Lights"),
    loc="upper left",
)
ax[0].title.set_text("Cell current as a function of voltage")

ax[0].grid()

ax[1].set_xlabel("Cell Voltage (V)")
ax[1].set_ylabel("Cell Power (W)")
ax[1].set_xlim([0, 0.7])
ax[1].set_ylim([0, 2])
ax[1].scatter(voltages4, powers4, color="r", marker="o", s=[1])
ax[1].scatter(voltages5, powers5, color="g", marker="v", s=[1])
ax[1].scatter(voltages6, powers6, color="b", marker="D", s=[1])
ax[1].scatter(voltages7, powers7, color="y", marker="o", s=[1])
ax[1].scatter(voltages8, powers8, color="k", marker="v", s=[1])
ax[1].legend(
    labels=("S Light", "N Light", "C Light", "NS Lights", "All Lights"),
    loc="upper left",
)
ax[1].title.set_text("Cell power as a function of voltage")
ax[1].grid()

plt.tight_layout()

fig.savefig("test.png")
plt.show()

# save into a file
with open("model.csv", "w", newline="\n") as csv_file:
    writer = csv.writer(csv_file)
    for idx in range(len(voltages4)):
        writer.writerow([voltages4[idx], currents4[idx], 255, 0, 0])
        writer.writerow([voltages5[idx], currents5[idx], 0, 255, 0])
        writer.writerow([voltages6[idx], currents6[idx], 0, 0, 255])
        writer.writerow([voltages7[idx], currents7[idx], 255, 255, 0])
        writer.writerow([voltages8[idx], currents8[idx], 0, 255, 255])