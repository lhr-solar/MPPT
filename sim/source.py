"""
Source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This file describes the Source class, which generates input values for the Display and MPPT.
"""

class Source:
    cycle = 0
    time_step = 1
    v_out = 0
    i_out = 0
    irradiance = 0
    temperature = 0
    load = 0

    def __init__(self):
        """
        init
        """
        return

    def read_data(self, file_name):
        """
        read_data 
        Takes a formatted file with the following types of values:
            - irradiance (W/m^2)
            - temperature (C)
            - load (W/s)
        A data structure in the Source is populated and these values are grabbed over time in iterate.

        Note: efficiency losses are not considered (as of yet) in the Source model.
        """
        return

    def read_data(self, irradiance, temperature, load):
        """
        read_data 
        Takes in several inputs:
            - irradiance (W/m^2)
            - temperature (C)
            - load (W/s)

        Note: efficiency losses are not considered (as of yet) in the Source model.
        """
        self.irradiance = irradiance
        self.temperature = temperature
        self.load = load

    def setup(self, cycle, time_step):
        self.cycle = cycle
        self.time_step = time_step
        return

    def iterate(self):
        """
        iterate
        Using a static set of values determined in init/managed by the user, or grabbed from a formatted file over each time step, iterate calculates the Vin, Iin, and Pmax the system should expect.
        """
        # TODO: using current timestep, load appropriate inputs and convert to v_out, i_out.
        return [self.v_out, self.i_out, self.cycle]

    def get_conditions(self):
        return [self.irradiance, self.temperature, self.load]
