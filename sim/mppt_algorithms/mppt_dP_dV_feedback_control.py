"""
mppt_dP_dV_feedback_control.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/28/20
Last Modified: 5/28/20
Description: dP/dV Feedback Control Algorithm.
"""
from .mppt import MPPT
class FC(MPPT):

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
            1. Modular Power Conditioning Unit for Photovoltaic Applications (Bhide et Bhat)
                - Section 3.4, Control Algorithm
                    - calculate the sign of dP/dV
                    - increase v_ref if sign is positive
                    - decrease v_ref if sign is negative
            2. Application of adaptive algorithm of solar cell battery charger (Hou et al.)
                - Section B, Implement of the control algorithm
        """
        if (cycle % self.sample_rate) is 0:
            if v_in is 0: # prevent from getting stuck when v_ref starts at 0
                v_in = .001
                
            error = .05
            p_in = v_in * i_in
            dP = p_in - self.p_old
            dV = v_in - self.v_old

            if dV == 0: # prevent division by 0 exception
                dV = .001

            dV_ref = self.calc_perturb_amt(self.v_ref, v_in, t_in)
            if abs(dP/dV) < error:
                self.v_ref += dV_ref
            else:
                if dP/dV > 0:
                    self.v_ref += dV_ref
                else:
                    self.v_ref -= dV_ref

            # update values
            self.v_old = v_in
            self.i_old = i_in
            self.p_old = p_in

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
        return "dP dV Feedback Control"