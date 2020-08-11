import sys

from cell import Cell
from simulation import Simulation
from mppt_algorithms.mppt_perturb_and_observe import PandO

env_regime = [
    [0, 0, 25],
    [1, 0, 25],
    [2, 0, 25],
    [3, 0, 25],
    [4, 0, 25],
    [5, 1000, 25],
    [10, 1000, 20],
    [20, 1000, 35],
    [30, 1000, 40],
    [40, 1000, 45],
    [50, 1000, 50],
    [60, 1000, 55],
    [70, 1000, 60],
    [80, 1000, 65],
    [85, 1000, 73.75],
    [90, 1000, 82],
    [95, 1000, 91.25],
    [100, 1000, 100],
    [110, 1000, 97.5],
    [120, 1000, 95],
    [130, 1000, 82.5],
    [140, 1000, 70],
    [150, 1000, 80],
    [160, 1000, 90],
    [165, 1000, 72.5],
    [170, 1000, 55],
    [175, 1000, 37.5],
    [180, 1000, 20],
    [185, 1000, 50],
    [190, 1000, 80],
    [195, 1000, 110],
    [200, 1000, 140]
]

# Nonideal model of a single cell impulse regime
cell = Cell("Nonideal")
cell.setup(setup_type="Array", regime=env_regime, impulse=(1000, 25))
# PandO MPPT running Fixed step stride
mppt = PandO()
v_ref = 0
stride = 0.05
sample_rate = 1
mppt.setup(v_ref, stride, sample_rate, "Fixed")
# Set up display
simulation = Simulation(mppt.get_name())
simulation.init_display()

# main loop
cycle = 0
max_cycle = 50
while cycle < max_cycle:
    if cycle%20 == 0:
        print("\nCycle: " + str(cycle))
    
    # get source power point
    (v_mpp, i_mpp, p_mpp) = cell.get_cell_gmpp()
    # get new values with the existing source after applying reference voltage
    (v_out, i_out, irrad, temp, load) = cell.iterate(v_ref)
    
    # update Simulation
    simulation.add_datapoint(cycle, irrad, temp, load, v_mpp, i_mpp, v_out, i_out)

    # pipe source into the mppt to find the new v_ref
    v_ref = mppt.iterate(v_out, i_out, temp, cycle)

    cycle = cell.increment_cycle()

# display the simulation and wait for exit
simulation.display(0, max_cycle, sample_rate)
input("Halted at the end of the cycle " + str(max_cycle))
