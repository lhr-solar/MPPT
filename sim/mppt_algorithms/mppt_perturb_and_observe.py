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
    v_ref = 0
    stride = 1
    sample_rate = 1

    p_old = 0
    v_old = 0

    def __init__(self):
        """
        init
        """
        return

    def setup(self, v_ref=0, stride=1, sample_rate=1):
        """
        setup
        Updates MPPT parameters
        
        Args:
            - v_ref (float): reference voltage (V)
            - stride (float): NOTE: UNUSED
            - sample_rate (int): cycles per iteration (1/Hz)
        Returns:
            - None
        """
        self.v_ref = v_ref
        self.stride = stride
        self.sample_rate = sample_rate

    def iterate(self, v_in, i_in, cycle):
        """
        iterate
        Runs a single iteration of the PandO algorithm.

        Args:
            - v_in (float): source voltage (V)
            - i_in (float): source current (A)
            - cycle (int): current simulation cycle
        Returns:
            - v_ref (float): output voltage (V)
        """
        if (cycle % self.sample_rate) is 0:
            # computer power
            p_new = v_in * i_in
            # determine deltas
            dP = p_new - self.p_old
            dV = v_in - self.v_old

            print("Power: ", p_new)
            print("Change Power: ", dP)
            print("Change Voltage: ", dV)

            if dP > 0:
                dV_ref = .01 #dV # calc_perturb_amt(v_ref, v_in)
                if dV > 0:  # increase v_ref
                    self.v_ref += dV_ref
                else:       # decrease v_ref
                    self.v_ref -= dV_ref
            elif dP < 0:
                dV_ref = .01 #dV # calc_perturb_amt(v_ref, v_in)
                if dV > 0:  # decrease v_ref
                    self.v_ref -= dV_ref
                else:       # increase v_Ref
                    self.v_ref += dV_ref

        # update values
        self.p_old = p_new
        self.v_old = v_in

        return self.v_ref

    # def calc_perturb_amt(self, v_ref, v_in):
    #     """
    #     calc_perturb_amt
    #     Uses a black box method to determine the change to v_ref

    #     Args:
    #         - v_ref (float): output reference voltage
    #         - v_in (float): source voltage
    #     Returns:
    #         - dV_ref (float): change in new reference voltage for current iteration
    #     NOTE: BLACK BOX THIS and swap out new methods
    #     """
    #     return 