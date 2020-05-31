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

from mppt_algorithms.mppt_perturb_and_observe import PandO
from mppt_algorithms.mppt_incremental_conduction import IC
# from mppt_algorithms.mppt_ripple_correlation_control import RCC
# from mppt_algorithms.mppt_fuzzy_logic import FL
from mppt_algorithms.mppt_dP_dV_feedback_control import FC

def main():
    # --------------PARAMETER PROMPTS--------------
    # source input dialogue
    string_source_model_type = input("Source Model type (see src docs): ['Benghanem']|'Ibrahim'|'Zahedi': ")
    source = Source(string_source_model_type)
    simulation = Simulation()
    # TODO: inputs to adjust rate of change of parameters to adjust model resolution

    # -------------- SIMULATION START --------------
    MAX_IRRADIANCE  = 1000  # W/M^2
    MAX_TEMPERATURE = 100   # C
    MAX_LOAD        = 0     # W
    irradiance = 0
    temperature = 0
    load = 0

    while irradiance < MAX_IRRADIANCE:
        source.setup_i(irradiance, temperature, load)
        # source gets the IV curve for current conditions
        [coordinates, [v_mpp, i_mpp, p_mpp]] = source.graph()

        # simulation.add_datapoint_source_model() # TODO: this

        # impulse update parameters here
        irradiance += 50
        # temperature += .5
        # load += UPDATE_HERE

    # simulation.display_source_model() # TODO: this



if __name__=="__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")

