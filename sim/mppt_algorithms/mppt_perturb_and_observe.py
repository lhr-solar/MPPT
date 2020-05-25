"""
PandO.py

P&O Algorithm function declarations
Fall 2017 MPPT using the Nucleo-L432KC (Pholociraptor)

Author: Samantha Guu
Team: Samuel Chiu, Madeline Drake, Kyle Grier, Rafael Ibanez, Chase Lansdale,
      Brooks Loper
Created on: November 12, 2017
Revised on: November 14, 2017
--------------------------------------------------------------------------------

Adapted by Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Last Modified: 5/24/20
"""

class PandO:
    delta_p = 0
    v_ref = 0
    sample_rate = 0

    def __init__(self):
        """
        init
        This function initializes anything needed the for P&O algo.

        Inputs: timingOn (bool)
        Outputs: none
        Errors: none
        """
        return

    def setup(self, v_ref, stride, sample_rate):
        self.v_ref = v_ref
        self.delta_p = stride
        self.sample_rate = sample_rate
        return

    def iterate(self, v_in, i_in, cycle):
        """
        iterate
        This function directs the flow of the Perturb and Observe algorithm
    
        Inputs: none (reads in 4 sensor values in subroutines)
        Outputs: none (changes global variable pulseWidth)
        Errors: none (pulseWidth error checks in pulseWidthErrorHandling subroutine)
        """
        if True: # TODO: (cycle % self.sample_rate) is 0:
            return 1 # TODO: implement PandO here
        else: 
            return None
