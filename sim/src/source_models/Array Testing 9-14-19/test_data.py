"""
test_data.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 8/16/20
Last Modified: 8/16/20
Description: Parses, cleans, and displays cell data collected from the 9-14-19 test.
    Rough and dirty script to grab some data to use for simulator testing. Use at your own risk.
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def round_num(x, prec=2, base=.05):
  return round(base * round(float(x)/base),prec)

f = open("Array Testing 9-14-19/Array2_Test2_9_14_19_fixed.dat", "r")
# remove first line with column headers
f.readline()

cycle = []
temp1 = []
temp2 = []

while True:
    # only read every five lines
    line = f.readline()

    if not line:
        break
    try:
        cycle.append(float(line.strip('\n').split(' ')[0]))
        temp1.append(float(line.strip('\n').split(' ')[1]))
        temp2.append(float(line.strip('\n').split(' ')[2]))
    except Exception as e:
        print(e)
    
    # number of lines to skip
    for i in range(30):
        line = f.readline()
        

fig, ax = plt.subplots(2, 1)
fig.set_size_inches(9, 10)

ax[0].set_xlabel('Cycle')
ax[0].set_ylabel('Temp 1')
ax[0].set_xlim([0, 5000])
ax[0].set_ylim([0, 150])
ax[0].scatter(cycle, temp1, color='r', marker='o', s=[1])
ax[0].title.set_text("Array temp 1 as a function of cycle")

ax[0].grid()

ax[1].set_xlabel('Cycle')
ax[1].set_ylabel('Temp 2')
ax[1].set_xlim([0, 5000])
ax[1].set_ylim([0, 150])
ax[1].scatter(cycle, temp2, color='r', marker='o', s=[1])
ax[1].title.set_text("Array temp 2 as a function of cycle")
ax[1].grid()

plt.tight_layout()

fig.savefig("test.png")
plt.show()

f = open("reformatted_data.txt", "w")
for idx in range(0, len(cycle)):
    line = "[" + str(idx) + ", " + str(1000) + ", " + str(round_num(temp1[idx], 1, .5)) + "],\n"
    f.write(line)

