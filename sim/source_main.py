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
    string_source_model_type = input("Source Model type (see src docs): ['Default']|'Benghanem'|'Ibrahim'|'Zahedi': ")
    source = Source(string_source_model_type)
    simulation = Simulation(string_source_model_type)
    # mode input dialogue
    string_mode = input("See effect of: ['Temperature']|'Irradiance'|'Load': ")
    # TODO: inputs to adjust rate of change of parameters to adjust model resolution

    # -------------- SIMULATION START --------------
    MAX_IRRADIANCE  = 1000  # W/M^2
    MAX_TEMPERATURE = 100   # C
    MAX_LOAD        = 0     # W
    irradiance = 0
    temperature = 0
    load = 0

    while irradiance <= MAX_IRRADIANCE and temperature <= MAX_TEMPERATURE and load <= MAX_LOAD :
        # input("Wait:")
        source.setup_i(irradiance, temperature, load)
        # source gets the IV curve for current conditions
        [coordinates, [v_mpp, i_mpp, p_mpp]] = source.graph()
        # print([coordinates, [v_mpp, i_mpp, p_mpp]])

        for coordinate in coordinates[:-1]:
            # print(coordinate)
            simulation.add_datapoint_source_model(irradiance, temperature, load, coordinate[0], coordinate[1])

        # impulse update parameters here
        if string_mode == "Irradiance":
            irradiance += 200
            temperature = 25 # fixed
        else:
            irradiance = 1000 # fixed
            temperature += 20
        # load += UPDATE_HERE

    simulation.display_source_model(string_mode)



if __name__=="__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")

