"""
mppt_ripple_correlation_control.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/28/20
Last Modified: 5/28/20
Description: Ripple Correlation Control Algorithm.
"""
from .mppt import MPPT
class RCC(MPPT):
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
            1. Dynamic maximum power point tracking of photovoltaic arrays using ripple correlation control (Esram et al)
                - TODO: figure this out
            2. Discrete-Time Ripple Correlation Control for Maximum Power Point Tracking. (Kimball et Krein)
                - TODO: figure this out
        """
        if (cycle % self.sample_rate) is 0:
            # switching ripple to optimize a cost function J, function of z
            # max value occurs at dJ/dZ = 0
            pass

        # update values
        self.v_old = v_in
        self.i_old = i_in

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
        return "Ripple Correlation Control"