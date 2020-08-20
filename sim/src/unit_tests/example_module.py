"""
example_module.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 8/10/20
Last Modified: 8/10/20

Description: This is an example program for the Array and MPPT Simulator to
showcase its functionality. It runs a simulation for a file with multiple modules.
    The simulator has three main components:
        1. Source simulator - The program simulates a solar cell or set of solar cells
        by taking in static parameters or a datafile of input values over time.
        2. MPPT Algorithm - A black box that manages algorithms (PandO, Incr.
        Conduction, RCC, Fuzzy Logic, etc) to maximize power on the load.
        3. Simulator - The outputs of the MPPT and the source are calculated, stored,
        and graphed. Data over time will be evaluated to determine and compare
        efficiencies between algorithms.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source import Source
from simulation import Simulation
from mppt_algorithms.mppt_perturb_and_observe import PandO

def main():
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
    single_cell = "single_cell.json"
    multi_cell = "two_cells_with_diode.json"

    # Nonideal model of a single cell impulse regime
    source = Source("Nonideal")
    source.setup(setup_type="File", file_name=multi_cell, regime=env_regime, impulse=(1000, 25))
    # PandO MPPT running Fixed step stride
    mppt = PandO()
    mppt.setup()
    # Set up display
    simulation = Simulation(mppt.get_name())
    simulation.init_display(source.get_num_cells())

    # main loop
    cycle = 0
    max_cycle = 50
    v_ref = 0
    while cycle < max_cycle:
        if cycle%20 == 0:
            print("\nCycle: " + str(cycle))
        
        # get source power point
        (v_mpp, i_mpp, p_mpp) = source.get_source_gmpp()

        # get new values with the existing source after applying reference voltage
        (v_out, i_out, irrad, temp, load) = source.iterate(v_ref)

        # update Simulation
        simulation.add_datapoint(cycle, irrad, temp, load, v_mpp, i_mpp, 0, 0)
        # print("[cycle, vsrc, isrc, psrc, vmppt, imppt, pmppt, temp, irrad, load]")
        # print(simulation.get_datapoint(cycle))

        # pipe source into the mppt to find the new v_ref
        print(
            "Cycle: ", cycle, 
            "\tV: {:.2f}".format(v_out), 
            "\tI: {:.2f}".format(i_out), 
            "\tP: {:.2f}".format(v_out*i_out)
        )
        v_ref = mppt.iterate(v_out, i_out, temp, cycle)

        # update cycle
        cycle = source.increment_cycle()

    # display the simulation and wait for exit
    simulation.display(0, max_cycle)
    input("Halted at the end of the cycle " + str(max_cycle))

if __name__=="__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")