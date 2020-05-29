"""
main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/28/20
Description: This is the main handler for the mppt simulator. 
  It uses Kivy for the UI of this application, in particular the graphs and statistics.
  The simulator has three main components:
      1. Source simulator - The program simulates a solar cell or set of solar cells by taking in static parameters or a datafile of input values over time.
      2. MPPT Algorithm - A black box that manages algorithms (PandO, Incr. Conduction, RCC, Fuzzy Logic, etc) to maximize power on the load.
      3. Simulator - The outputs of the MPPT and the source are calculated, stored, and graphed. Data over time will be evaluated to determine and compare efficiencies between algorithms.
"""
from source import Source
from simulation import Simulation

from mppt_algorithms.mppt_perturb_and_observe import PandO
from mppt_algorithms.mppt_incremental_conduction import IC
# from mppt_algorithms.mppt_ripple_correlation_control import RCC
# from mppt_algorithms.mppt_fuzzy_logic import FL
from mppt_algorithms.mppt_dP_dV_feedback_control import FC

def main():
    profile_file_path = ""
    mode_profile = False

    source = Source()

    # model input dialogue
    mppt = None
    string_model_type = input("Model type: ['PandO']|'IC'|'FC': ")
    if string_model_type == "IC":
        mppt = IC()
    elif string_model_type == "FC":
        mppt = FC()
    else:
        mppt = PandO()
    simulation = Simulation(mppt.get_name())

    # parameters input dialogue
    # NOTE: Modify these values
    max_cycle = 350
    sample_rate = 1
    v_ref = 0
    temp_regime = [
        [0, 25],
        [10, 20],
        [20, 35],
        [30, 40],
        [40, 45],
        [50, 50],
        [60, 55],
        [70, 60],
        [80, 65],
        [85, 73.75],
        [90, 82],
        [95, 91.25],
        [100, 100],
        [110, 97.5],
        [120, 95],
        [130, 82.5],
        [140, 70],
        [150, 80],
        [160, 90],
        [165, 72.5],
        [170, 55],
        [175, 37.5],
        [180, 20],
        [185, 50],
        [190, 80],
        [195, 110],
        [200, 140]
    ]
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



    string_profile = input("Profile ['impulse']|'profile': ")
    if string_profile == "profile":
        mode_profile = True

    # simulating from a dataset
    if mode_profile is True:
        print("Running in Profile mode.")
        profile_type = input("Profile type ['array']|'file': ")

        if profile_type == "file":
            profile_file_path = input("Enter filepath: ")
            # read in data and setup settings
            if source.setup_f(profile_file_path): # this loads the arrays in the source for us
                # simulation only
                time_step   = 1
                cycle_start = 0
                cycle_end   = 0
                # for source and simulation
                cycle = 0
                # mppt only
                stride = 0
                mppt.setup(v_ref, stride, sample_rate)

                while cycle <= max_cycle: # simulator main loop
                    print("\nCycle: " + str(cycle))

                    # generate outputs for source
                    [v_src, i_src, irrad, temp, load] = source.iterate_t(v_ref, cycle)
                    print("Source: " + str([v_src, i_src, irrad, temp, load]))

                    # pipe source into the mppt
                    v_ref = mppt.iterate(v_src, i_src, temp, cycle)

                    # update Simulation with new values
                    simulation.addDatapoint(cycle, irrad, temp, load, v_src, i_src, v_ref)
                    print(simulation.getDatapoint(cycle))

                    # update cycle
                    cycle += 1
            
                # display Simulation windows
                simulation.display(cycle_start, max_cycle, time_step)
                input("Halted at the end of cycle " +  str(max_cycle))
            else:
                print("Unsuccessful load. Exiting.")
        else:
            source.setup_a(temp_regime)
            # simulation only
            time_step   = 1
            cycle_start = 0
            # for source and simulation
            cycle = 0
            # mppt only
            stride = 0
            mppt.setup(v_ref, stride, sample_rate)

            while cycle <= max_cycle: # simulator main loop
                print("\nCycle: " + str(cycle))

                # generate outputs for source
                [v_src, i_src, irrad, temp, load] = source.iterate_t(v_ref, cycle)
                print("Source: " + str([v_src, i_src, irrad, temp, load]))

                # pipe source into the mppt
                v_ref = mppt.iterate(v_src, i_src, temp, cycle)

                # update Simulation with new values
                simulation.addDatapoint(cycle, irrad, temp, load, v_src, i_src, v_ref)
                print(simulation.getDatapoint(cycle))

                # update cycle
                cycle += 1
            
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
        irradiance  = 0
        temperature = 25
        load        = 0

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
        source.setup_i(irradiance, temperature, load)
        # mppt only
        stride = 0
        #initialize startup values into the mppt
        mppt.setup(v_ref, stride, sample_rate)

        while cycle <= max_cycle: # simulator main loop
            print("\nCycle: " + str(cycle))
    
            [v_src, i_src] = source.iterate(v_ref)
            print("Source: " + str([v_src, i_src]))

            # pipe source into the mppt
            v_ref = mppt.iterate(v_src, i_src, temperature, cycle)
            print(v_ref)

            # update Simulation with new values
            simulation.addDatapoint(cycle, irradiance, temperature, load, v_src, i_src, v_ref)
            print("[cycle, vsrc, isrc, psrc, vref, pref, temp, irrad, load]")
            print(simulation.getDatapoint(cycle))

            # update cycle
            cycle += 1
            # impulse update parameters
            # temperature += .5
            source.setup_i(irradiance, temperature, load)
        
        # display Simulation windows
        simulation.display(cycle_start, max_cycle, time_step)
        input("Halted at the end of cycle " +  str(max_cycle))

if __name__=="__main__":
    main()
else:
    print("Run main.py as a script.")

