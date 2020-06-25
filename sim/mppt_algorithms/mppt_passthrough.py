"""
mppt_passthrough.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/28/20
Last Modified: 6/24/20
Description: MPPT passthrough algorithm. Essentially lets the stride function determine where to go.
"""
from .mppt import MPPT
class PT(MPPT):

    # overload iterate method
    def iterate(self, v_in, i_in, t_in, cycle):
        """
        iterate
        Runs a single iteration of the hill climbing algorithm defined in mppt/calc_perturb_amt().

        Args:
            - v_in (float): source voltage (V)
            - i_in (float): source current (A)
            - t_in (float): temperature
            - cycle (int): current simulation cycle

        Returns:
            - v_ref (float): output voltage (V)

        Ref:
            None
        """
        if (cycle % self.sample_rate) is 0:
            self.v_ref = self.calc_perturb_amt(self.v_ref, v_in, i_in, t_in)
            p_in = v_in * i_in

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
        return "Passthrough"