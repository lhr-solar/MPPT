"""
main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This is the main handler for the mppt simulator. 
  It uses Kivy for the UI of this application, in particular the graphs and statistics.
  The simulator has three main components:
      1. Source simulator - The program simulates a solar cell or set of solar cells by taking in static parameters or a datafile of input values over time.
      2. MPPT Algorithm - A black box that manages algorithms (PandO, Incr. Conduction, RCC, Fuzzy Logic, etc) to maximize power on the load.
      3. Display - The outputs of the MPPT and the source are calculated and graphed. Data over time will be evaluated to determine and compare efficiencies between algorithms.
"""
from source import Source

# TODO: create a generic container to manage these imports and set `mppt = MPPT(x)?`
from mppt_algorithms.mppt_perturb_and_observe import PandO
# from mppt_incremental_conduction import IC
# from mppt_ripple_correlation_control import RCC
# from mppt_fuzzy_logic import FL
# from mppt_fraction_open_circuit_voltage import FOCV

# from gui.display import DisplayApp

def main():
    profile_file_path = ""
    source = None
    mode_profile = False
    looping = True
    waiting = True

    source = Source()

    # display = DisplayApp()
    # display.run()
    mppt = PandO()

    tmp_storage = None

    # simulating from a dataset
    if mode_profile is True:
        # read in data and setup settings
        source.read_data(profile_file_path)
        # initialize to the start of the simulation
        cycle = 0
        time_step = 1
        source.setup(0, time_step) # TODO: adjust start params

        # setup mppt
        v_ref = 0
        stride = 0
        sample_rate = 1
        mppt.setup(v_ref, stride, sample_rate)

        while looping:
            # halt every loop for use input or disable halt
            if waiting: 
                # TODO: call setup again when user rewinds/etc
                source.setup(cycle, time_step)
                mppt.setup(v_ref, stride, sample_rate)

            # generate value for source, it also generates the current cycle
            [v_out, i_out, cycle] = source.iterate()

            # pipe source into the mppt
            v_ref = mppt.iterate(v_out, i_out, cycle)

            if v_ref is None: # MPPT is not sampling this cycle
                pass
            else: # MPPT has sampled this cycle
                p_max = v_out * i_out
                p_out = v_ref * i_out
                [irradiance, temperature, load] = source.get_conditions()
                tmp_storage = [cycle, irradiance, temperature, load, v_out, i_out, p_max, v_ref, p_out]
                # TODO:value goes into storage

    # simulating from an impulse created by the user
    else:
        # setup source
        irradiance = 0
        temperature = 0
        load = 0
        cycle = 0
        time_step = 1
        # initialize nothing into read_data
        source.read_data(irradiance, temperature, load)
        # initialize to the start of the simulation
        source.setup(cycle, time_step) 

        # setup mppt
        v_ref = .6
        stride = 0
        sample_rate = 1
        mppt.setup(v_ref, stride, sample_rate)

        while looping:
            # halt every loop for use input or disable halt
            input("\nCycle: " + str(cycle))
            if waiting: 
                # TODO: call setup again when user rewinds/etc
                source.setup(cycle, time_step)
                mppt.setup(v_ref, stride, sample_rate)

            # generate value for source, it also generates the current cycle
            [v_out, i_out, cycle] = source.iterate(v_ref)

            print("Source: " + str([v_out, i_out, cycle]))

            # pipe source into the mppt
            v_ref = mppt.iterate(v_out, i_out, cycle)

            p_max = v_out * i_out
            p_out = v_ref * i_out
            tmp_storage = [cycle, irradiance, temperature, load, v_out, i_out, p_max, v_ref, p_out]
            # TODO:value goes into display storage
            print("cycle [v_out i_out p_max v_ref p_out]")
            print(tmp_storage[0], tmp_storage[4::])






if __name__=="__main__":
    main()
else:
    print("Run main.py as a script.")
