"""
mppt_perturb_and_observe.py

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
Last Modified: 5/28/20
"""
from .mppt import MPPT
class PandO(MPPT):
    # overload iterate method
    def iterate(self, v_in, i_in, t_in, cycle):
        """
        iterate TODO: Add paper
        Runs a single iteration of the PandO algorithm.

        Args:
            - v_in (float): source voltage (V)
            - i_in (float): source current (A)
            - t_in (float): temperature
            - cycle (int): current simulation cycle
            
        Returns:
            - v_ref (float): output voltage (V)
        """
        if (cycle % self.sample_rate) is 0: #sampling this run
            if v_in is 0: # prevent from getting stuck when v_ref starts at 0
                v_in = .001

            # compute power
            p_new = v_in * i_in
            # determine deltas
            dP = p_new - self.p_old
            dV = v_in - self.v_old

            print("Power: ", p_new)
            print("Change Power: ", dP)
            print("Change Voltage: ", dV)

            dV_ref = self.calc_perturb_amt(self.v_ref, v_in, t_in)
            if dP > 0:
                if dV > 0:  # increase v_ref
                    self.v_ref += dV_ref
                else:       # decrease v_ref
                    self.v_ref -= dV_ref
            elif dP < 0:
                if dV > 0:  # decrease v_ref
                    self.v_ref -= dV_ref
                else:       # increase v_Ref
                    self.v_ref += dV_ref

            # update values
            self.p_old = p_new
            self.v_old = v_in

        return self.v_ref

    def get_name(self):
        """
        get_name
        Returns mppt algorithm name.
        
        Args:
            - None

        Returns:
            - Name (String)
        """
        return "Perturb and Observe"