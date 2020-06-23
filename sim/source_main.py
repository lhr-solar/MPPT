"""
source_main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/31/20
Last Modified: 5/31/20
Description: This file emulatea source IV curves across multiple dimensions.

"""
import sys

from source import Source
from simulation import Simulation

def main():
    # --------------PARAMETER PROMPTS--------------
    # source input dialogue
    string_source_model_type = input("Source Model type (see src docs): ['Default'/'Nonideal']|'Ideal': ")
    source = Source(string_source_model_type)
    simulation = Simulation(source.get_model_name())
    # mode input dialogue
    string_mode = input("See effect of: ['Temperature']|'Irradiance'|'Load': ")
    if string_mode != "Irradiance" and string_mode != "Load":
        string_mode = "Temperature"

    step_size_v = .01
    step_size_t = 20
    step_size_i = 200

    # voltage step size
    string_step_size_v = input("Voltage Step Size ['" + str(step_size_v) + "']: ")
    try:
        tmp_step_size_v = float(string_step_size_v)
        step_size_v = tmp_step_size_v
    except ValueError:
        print("Invalid integer. Defaulting to", step_size_v, "step size.")

    if string_mode == "Irradiance": # irradiance step size
        string_step_size_i = input("Irradiance Step Size ['" + str(step_size_i) + "']: ")
        try:
            tmp_step_size_i = int(string_step_size_i)
            step_size_i = tmp_step_size_i
        except ValueError:
            print("Invalid integer. Defaulting to", step_size_i, "step size.")
    else: # temperature step size
        string_step_size_t = input("Temperature Step Size ['" + str(step_size_t) + "']: ")
        try:
            tmp_step_size_t = int(string_step_size_t)
            step_size_t = tmp_step_size_t
        except ValueError:
            print("Invalid integer. Defaulting to", step_size_t, "step size.")

    # -------------- SIMULATION START --------------
    MAX_IRRADIANCE  = 1000  # W/M^2
    MAX_TEMPERATURE = 100   # C
    MAX_LOAD        = 0     # W
    irradiance = 0.001
    temperature = 0.001
    load = 0

    # impulse update parameters here
    if string_mode == "Irradiance":
        irradiance = 0.001
        temperature = 25 # fixed
    else:
        irradiance = 1000 # fixed
        temperature = 0

    while irradiance <= MAX_IRRADIANCE and temperature <= MAX_TEMPERATURE and load <= MAX_LOAD :
        # input("Wait:")
        source.setup_i(irradiance, temperature, load)
        # source gets the IV curve for current conditions
        [coordinates, [v_mpp, i_mpp, p_mpp]] = source.graph(step_size_v)
        # print([coordinates, [v_mpp, i_mpp, p_mpp]])

        for coordinate in coordinates[:-1]:
            # print(coordinate)
            simulation.add_datapoint_source_model(irradiance, temperature, load, coordinate[0], coordinate[1])

        # impulse update parameters here
        if string_mode == "Irradiance":
            irradiance += step_size_i
            temperature = 25 # fixed
        else:
            irradiance = 1000 # fixed
            temperature += step_size_t
        # load += UPDATE_HERE

    simulation.display_source_model(string_mode)



if __name__=="__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")

