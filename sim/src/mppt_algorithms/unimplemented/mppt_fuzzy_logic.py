"""
mppt_fuzzy_logic.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/28/20
Last Modified: 5/28/20
Description: Fuzzy Logic Algorithm.
"""
from .mppt import MPPT
class FL(MPPT):
    # TODO: define a linguistic rule table
    # NOTE: rules in the table are based on power convert and user
    err_old = 0

    # overload iterate method
    def iterate(self, v_in, i_in, t_in, cycle):
        """
        iterate
        Runs a single iteration of the PandO algorithm.

        Args:
            - v_in (float): source voltage (V)
            - i_in (float): source current (A)
            - t_in (float): temperature
            - cycle (int): current simulation cycle

        Returns:
            - v_ref (float): output voltage (V)

        Ref:
            1. Fuzzy logic controller based maximum power point tracking for pv system (Narendiran et al)
                - TODO: figure this out
        """
        if (cycle % self.sample_rate) is 0:
            p_in = v_in * i_in
            err = (p_in - self.p_old)/(v_in - self.v_old)
            dE = err - self.err_old

            # TODO: determine state from rule table
            # TODO: based on state do action

            # change is based on error competition

            # update values
            self.v_old = v_in
            self.i_old = i_in
            self.err = err

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
        return "Fuzzy Logic"