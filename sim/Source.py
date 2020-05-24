"""
Source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This file describes the Source class, which generates input values for the Display and MPPT.
"""

class Source:
    def __init__(self):
        """
        init
        """
        return

    def read_data():
        """
        read_data 
        Takes a formatted file with the following types of values:
            - irradiance (W/m^2)
            - temperature (C)
            - load (W/s)
        A data structure in the Source is populated and these values are grabbed over time in iterate.

        Note: efficiency losses are not considered (as of yet) in the Source model.
        """

    def iterate():
        """
        iterate
        Using a static set of values determined in init/managed by the user, or grabbed from a formatted file over each time step, iterate calculates the Vin, Iin, and Pmax the system should expect.
        """
        return
