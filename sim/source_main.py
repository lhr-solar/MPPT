"""
source_main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/31/20
Last Modified: 8/20/20
Description: This file emulates a single cell source IV curve across multiple dimensions.

"""
import sys
import time
from src.source import Source
from src.simulation import Simulation
from src.source_file import SourceFile

def main():
    # --------------PARAMETER PROMPTS--------------
    # source input dialogue
    print("Suggested save parameters are: v=0.01, i=50, t=.5.")
    print("Suggested display parameters are: v=0.01, i=50, t=5.")

    string_source_model_type = input("Source Model type (see src docs): ['Default'/'Nonideal']|'Ideal': ")
    step_size_v = .01
    step_size_i = 50
    step_size_t = .5

    # voltage step size
    string_step_size_v = input("Voltage Step Size ['" + str(step_size_v) + "']: ")
    try:
        tmp_step_size_v = float(string_step_size_v)
        step_size_v = tmp_step_size_v
    except ValueError:
        print("Invalid float. Defaulting to", step_size_v, "step size.")

    # irradiance step size
    string_step_size_i = input("Irradiance Step Size ['" + str(step_size_i) + "']: ")
    try:
        tmp_step_size_i = float(string_step_size_i)
        step_size_i = tmp_step_size_i
    except ValueError:
        print("Invalid float. Defaulting to", step_size_i, "step size.")

    # temperature step size
    string_step_size_t = input("Temperature Step Size ['" + str(step_size_t) + "']: ")
    try:
        tmp_step_size_t = float(string_step_size_t)
        step_size_t = tmp_step_size_t
    except ValueError:
        print("Invalid float. Defaulting to", step_size_t, "step size.")

    string_disp_sim = input("Display output graphs [NO]|YES: ")
    disp_sim = False
    if string_disp_sim == "YES":
        disp_sim = True
    
    string_save_sim = input("Save output model [NO]|YES: ")
    save_sim = False
    use_file = True
    if string_save_sim == "YES":
        save_sim = True
        use_file = False

    is_overlay = ""
    if disp_sim:
        string_is_overlay = input("Load irradiance data? File format should be 'V,C,R,G,B', ... - [NO]|FILE_PATH: ")
        if string_is_overlay != "NO":
            is_overlay = string_is_overlay

    source = Source(string_source_model_type, use_file=use_file)
    simulation = Simulation(source.get_model_type())
    source_file = SourceFile()

    # -------------- SIMULATION START --------------
    MAX_VOLTAGE     = 0.8
    MAX_IRRADIANCE  = 1000  # W/M^2
    MAX_TEMPERATURE = 80    # C
    MAX_LOAD        = 0     # W
    irradiance = 0.001
    temperature = 0.001
    load = 0

    # set up output file results
    num_bins = int(MAX_VOLTAGE/step_size_v)+1 # add one just to make sure we always have more bins than characteristics
    results = []
    for bin in range(num_bins):
        results.append([])

    print("Start model generation.")
    start = time.time()
    source.setup("Impulse", impulse=(irradiance, temperature))

    # cycle outside through inside
    while irradiance <= MAX_IRRADIANCE:
        temperature = 0.001
        while temperature <= MAX_TEMPERATURE:
            modules = source.get_modules()
            for module in modules:
                module[2].setup("Impulse", impulse=(irradiance, temperature))
            # source gets the IV curve for current conditions
            [characteristics, [v_mpp, i_mpp, p_mpp]] = source.get_source_IV(step_size_v)

            bin_num = 0
            for characteristic in characteristics:
                # we want the voltage to be on the very outside, so we sort by bins
                results[bin_num].append([
                    round(characteristic[0], 3), 
                    round(irradiance, 3), 
                    round(temperature, 3), 
                    round(characteristic[1], 3)
                ])
                if disp_sim:
                    simulation.add_datapoint_source_model(
                        round(irradiance, 3), 
                        round(temperature, 3), 
                        0,
                        round(characteristic[0], 3), 
                        round(characteristic[1], 3)
                    )
                    # simulation.update_display_source_model()

                bin_num += 1

            if temperature == 0.001:
                temperature = 0
            temperature += step_size_t
        if irradiance == 0.001:
            irradiance = 0
        irradiance += step_size_i

    for bin in results:
        for entry in bin:
            source_file.add_source(entry)
    if save_sim:
        source_file.write_file()
        
    end = time.time()
    print("Build time: ", (end - start))

    if disp_sim:
        print("Showing display.")
        simulation.init_display_source_model(file=is_overlay)
        simulation.update_display_source_model()
    
    input("Waiting.")

if __name__=="__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")

