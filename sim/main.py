"""
main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 8/10/20
Description: This is the main handler for the mppt simulator. 
    The simulator has three main components:
      1. Source simulator - The program simulates a solar cell or set of solar cells by taking in static parameters or a datafile of input values over time.
      2. MPPT Algorithm - A black box that manages algorithms (PandO, Incr. Conduction, RCC, Fuzzy Logic, etc) to maximize power on the load.
      3. Simulator - The outputs of the MPPT and the source are calculated, stored, and graphed. Data over time will be evaluated to determine and compare efficiencies between algorithms.
"""
import sys

from cell import Cell
from simulation import Simulation

from mppt_algorithms.mppt_perturb_and_observe import PandO
from mppt_algorithms.mppt_incremental_conduction import IC
# from mppt_algorithms.mppt_ripple_correlation_control import RCC
# from mppt_algorithms.mppt_fuzzy_logic import FL
from mppt_algorithms.mppt_dP_dV_feedback_control import FC
from mppt_algorithms.mppt_passthrough import PT

def main():
    profile_file_path = ""
    mode_profile = False

    # NOTE: Modify these values
    max_cycle = 350
    sample_rate = 1
    stride = .05
    v_ref = 0
    stride_mode = None
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

    # --------------PARAMETER PROMPTS--------------
    # source input dialogue
    string_source_model_type = input("Source Model type (see src docs): ['Nonideal']|'Ideal': ")
    source = Cell(string_source_model_type)

    # model input dialogue
    mppt = None
    string_mppt_algorithm_type = input("MPPT Algorithm type: ['PandO']|'IC'|'FC'|'Passthrough': ")
    if string_mppt_algorithm_type == "IC":
        mppt = IC()
    elif string_mppt_algorithm_type == "FC":
        mppt = FC()
    elif string_mppt_algorithm_type == "Passthrough":
        mppt = PT()
    else:
        mppt = PandO()
    simulation = Simulation(mppt.get_name())

    # mppt stride mode dialogue
    if string_mppt_algorithm_type == "Passthrough":
        string_stride_mode = input("Stride mode for MPPT (see src docs): ['Golden']|'Ternary'|'Bisection'|'Newton(X)'|'BFGS(X)': ")
        if string_stride_mode == "Golden" or string_stride_mode == "Ternary" or string_stride_mode == "Bisection" or string_stride_mode == "Newton" or string_stride_mode == "BFGS":
            stride_mode = string_stride_mode
            print(stride_mode)
    else:
        string_stride_mode = input("Stride mode for MPPT (see src docs): ['Fixed']|'Adaptive'|'Optimal': ")
        if string_stride_mode == "Fixed" or string_stride_mode == "Optimal" or string_stride_mode == "Adaptive":
            stride_mode = string_stride_mode

    # profile input dialogue
    string_profile = input("Profile ['impulse']|'profile': ")
    if string_profile == "profile":
        mode_profile = True
        
    # parameter input dialogue
    string_max_cycle = input("Max cycle ['" + str(max_cycle) + "']: ")
    try:
        tmp_max_cycle = int(string_max_cycle)
        max_cycle = tmp_max_cycle
    except ValueError:
        print("Invalid integer. Defaulting to", max_cycle, "cycles.")
    string_sample_rate = input("Sample rate ['" + str(sample_rate) + "']: ")
    try:
        tmp_sample_rate = int(string_sample_rate)
        sample_rate = tmp_sample_rate
    except ValueError:
        print("Invalid integer. Defaulting to a sample every " + str(sample_rate) + " cycles.")
    string_v_ref = input("Starting mppt output voltage ['" + str(v_ref) + "']: ")
    try:
        tmp_v_ref = float(string_v_ref)
        v_ref = tmp_v_ref
    except ValueError:
        print("Invalid integer. Defaulting to a cycle 0 v_ref of " + str(v_ref) + " V.")
    string_stride = input("Default stride (for fixed stride function) ['" + str(stride) + "']: ")
    try:
        tmp_stride = float(string_stride)
        stride = tmp_stride
    except ValueError:
        print("Invalid integer. Defaulting to stride of " + str(stride) + ".")


    # -------------- SIMULATION START --------------
    # simulating from a dataset
    if mode_profile is True:
        print("Running in Profile mode.")

        source.setup("Array", env_regime)
        # simulation only
        time_step   = 1
        cycle_start = 0
        # for source and simulation
        cycle = 0
        # mppt only
        v_mppt = 0
        i_mppt = 0
        mppt.setup(v_ref, stride, sample_rate, stride_mode)

        simulation.init_display()
        while cycle <= max_cycle: # simulator main loop
            if cycle%20 == 0:
                print("\nCycle: " + str(cycle))

            # get source power point
            (v_mpp, i_mpp, p_mpp) = source.get_cell_gmpp()
            # get new values with the existing source after applying reference voltage
            (v_out, i_out, irrad, temp, load) = source.iterate(v_ref)
            
            # update Simulation
            simulation.add_datapoint(cycle, irrad, temp, load, v_mpp, i_mpp, v_out, i_out)
            # print("[cycle, vsrc, isrc, psrc, vmppt, imppt, pmppt, temp, irrad, load]")
            # print(simulation.get_datapoint(cycle))

            # pipe source into the mppt to find the new v_ref
            v_ref = mppt.iterate(v_out, i_out, temp, cycle)

            # update cycle
            cycle = source.increment_cycle()
        
        # display Simulation windows
        simulation.display(cycle_start, max_cycle, time_step)
        input("Halted at the end of cycle " +  str(max_cycle))

    # simulating from an impulse created by the user
    else:
        print("Running in Impulse mode.")
        # simulation only
        time_step   = 1
        cycle_start = 0
        # for source and simulation
        cycle       = 0
        irradiance  = 1000
        temperature = 25
        load        = 0
        # mppt
        v_mppt      = 0
        i_mppt      = 0

        string_irrad = input("Starting irradiance ['" + str(irradiance) + "']: ")
        try:
            tmp_irrad = float(string_irrad)
            irradiance = tmp_irrad
        except ValueError:
            print("Invalid integer. Defaulting to an irradiance of " + str(irradiance) + " W/m^2.")

        string_temp = input("Starting temperature ['" + str(temperature) + "']: ")
        try:
            tmp_temp = float(string_temp)
            temperature = tmp_temp
        except ValueError:
            print("Invalid integer. Defaulting to a temperature of " + str(temperature) + " C.")

        string_load = input("Starting load ['" + str(load) + "']: ")
        try:
            tmp_load = float(string_load)
            load = tmp_load
        except ValueError:
            print("Invalid integer. Defaulting to a load of " + str(load) + " W.")

        input("Ready to start. Press enter to run the simulation.")

        # initialize startup values into the source
        source.setup("Impulse", impulse=(irradiance, temperature))
        #initialize startup values into the mppt
        mppt.setup(v_ref, stride, sample_rate, stride_mode)

        simulation.init_display()
        while cycle <= max_cycle: # simulator main loop
            if cycle%20 == 0:
                print("\nCycle: " + str(cycle))

            # get source power point
            (v_mpp, i_mpp, p_mpp) = source.get_cell_gmpp()
            # get new values with the existing source after applying reference voltage
            (v_out, i_out, irrad, temp, load) = source.iterate(v_ref)
            
            # update Simulation
            simulation.add_datapoint(cycle, irrad, temp, load, v_mpp, i_mpp, v_out, i_out)
            # print("[cycle, vsrc, isrc, psrc, vmppt, imppt, pmppt, temp, irrad, load]")
            # print(simulation.get_datapoint(cycle))

            # pipe source into the mppt to find the new v_ref
            v_ref = mppt.iterate(v_out, i_out, temp, cycle)

            # update cycle
            cycle = source.increment_cycle()
            # impulse update parameters here
            # irradiance += UPDATE_HERE
            # temperature += .5
            # load += UPDATE_HERE
            # source.setup_i(irradiance, temperature, load)
        
        # display Simulation windows
        simulation.display(cycle_start, max_cycle, time_step)
        input("Halted at the end of cycle " +  str(max_cycle))

if __name__=="__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")

