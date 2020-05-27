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
from simulation import Simulation
# TODO: create a generic container to manage these imports and set `mppt = MPPT(x)?`
from mppt_algorithms.mppt_perturb_and_observe import PandO
from mppt_algorithms.mppt_incremental_conduction import IC
# from mppt_algorithms.mppt_ripple_correlation_control import RCC
# from mppt_algorithms.mppt_fuzzy_logic import FL
# from mppt_algorithms.mppt_fraction_open_circuit_voltage import FOCV

# from gui.display import DisplayApp

def main():
    profile_file_path = ""
    mode_profile = False

    source = Source()
    mppt = IC()
    simulation = Simulation()


    profile_string = input("Profile ['impulse']|'profile': ")
    if profile_string == "profile":
        mode_profile = True

    # simulating from a dataset
    if mode_profile is True:
        print("Running in Profile mode.")
        profile_file_path = input("Enter filepath: ")


        # read in data and setup settings
        if source.read_data(profile_file_path): # this loads the arrays in the source for us
            # simulation only
            time_step   = 1
            cycle_start = 0
            cycle_end   = 0
            # for source and simulation
            cycle = 0

            # mppt only
            v_ref = 0 
            stride = 0
            sample_rate = 1
            mppt.setup(v_ref, stride, sample_rate)

            while True: # simulator main loop
                
                print("\nCycle: " + str(cycle))
                command_string = input("Command ['step']|'change_param': ")

                if command_string == "change_param": 
                    pass
                    # TODO: call setup again when user rewinds/etc
                    # rewind time

                # generate outputs for source
                [v_src, i_src, irrad, temp, load] = source.iterate_t(v_ref, cycle)
                print("Source: " + str([v_src, i_src, irrad, temp, load]))

                # pipe source into the mppt
                v_ref = mppt.iterate(v_src, i_src, temp, cycle)

                # update Simulation with new values
                simulation.addDatapoint(cycle, irrad, temp, load, v_src, i_src, v_ref)
                print(simulation.getDatapoint(cycle))

                # display Simulation windows
                cycle_end = cycle # TODO: control this later
                simulation.display(cycle_start, cycle_end, time_step)

                # update cycle
                cycle += 1
        else:
            print("Unsuccessful load. Exiting.")

    # simulating from an impulse created by the user
    else:
        print("Running in Impulse mode.")
        # simulation only
        time_step   = 1
        cycle_start = 0
        cycle_end   = 0
        # for source and simulation
        cycle       = 0
        irradiance  = 0
        temperature = 25
        load        = 0
        # initialize startup values into the source
        source.setup(irradiance, temperature, load)

        # mppt only
        v_ref = .35 #TODO: mppt doesn't change v_ref if initialized to 0 at the start since dP is 0
        stride = 0
        sample_rate = 1
        #initialize startup values into the mppt
        mppt.setup(v_ref, stride, sample_rate)

        test_v = .4

        while True: # simulator main loop
            
            print("\nCycle: " + str(cycle))
            command_string = input("Command ['step']|'change_param': ")

            if command_string == "change_param": 
                pass
                # TODO: call setup again when user rewinds/etc
                # rewind time
                # new impulse
                    # source.setup(irradiance, temperature, load)
                    # mppt.setup(v_ref, stride, sample_rate)

            # generate outputs for source
            
            [v_src, i_src] = source.iterate(v_ref)
            print("Source: " + str([v_src, i_src]))



            # pipe source into the mppt
            v_ref = mppt.iterate(v_src, i_src, temperature, cycle)
            print(v_ref)

            # update Simulation with new values
            simulation.addDatapoint(cycle, irradiance, temperature, load, v_src, i_src, v_ref)
            print("[cycle, vsrc, isrc, psrc, vref, pref, temp, irrad, load]")
            print(simulation.getDatapoint(cycle))

            # display Simulation windows
            cycle_end = cycle # TODO: control this later
            simulation.display(cycle_start, cycle_end, time_step)

            # update cycle
            cycle += 1
            if cycle%20 == 0:
                temperature += 10
                # test_v = .4
                source.setup(irradiance, temperature, load)
            # test_v += .02





if __name__=="__main__":
    main()
else:
    print("Run main.py as a script.")

