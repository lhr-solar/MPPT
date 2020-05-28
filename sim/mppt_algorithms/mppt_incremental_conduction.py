"""
mppt_incremental_conduction.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/25/20
Last Modified: 5/28/20
Description: Incremental Conduction Algorithm.
"""
from .mppt import MPPT
class IC(MPPT):
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
        if (cycle % self.sample_rate) is 0: # sampling this run
            if v_in is 0: # prevent from getting stuck when v_ref starts at 0
                v_in = .001

            # determine deltas
            dV = v_in - self.v_old
            dI = i_in - self.i_old

            print("Change Voltage: ", dV)
            print("Change Current: ", dI)

            dV_ref = self.calc_perturb_amt(self.v_ref, v_in, t_in)
            if dV == 0:
                if dI == 0:
                    pass
                else:
                    if dI > 0:
                        self.v_ref -= dV_ref
                    else:
                        self.v_ref += dV_ref
            else:
                dC = (i_in + (dI / dV) * v_in) # instantaneous conductance
                print("Incremental Conductance: ", dC)
                if dI/dV == -i_in/v_in:
                    pass
                else:
                    if dI/dV > -i_in/v_in:
                        self.v_ref += dV_ref
                    else:
                        self.v_ref -= dV_ref

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
        return "Incremental Conductance"