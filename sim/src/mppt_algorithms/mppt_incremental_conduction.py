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
        iterate
        Runs a single iteration of the PandO algorithm.

        Args:
            - v_in (float): source voltage (V)
            - i_in (float): source current (A)
            - t_in (float): temperature (C)
            - cycle (int): current simulation cycle

        Returns:
            - v_ref (float): output voltage (V)

        Ref:
            1. Incremental Conductance Based Maximum Power Point Tracking (MPPT) for Photovoltaic System (Lokanadham et Bhaskar)
                - VI. Incremental Conductance MPPT Algorithm
        """
        if (cycle % self.sample_rate) == 0: # sampling this run
            # determine deltas
            dV = v_in - self.v_old
            dI = i_in - self.i_old

            print("[IC] Change Voltage: ", dV)
            print("[IC] Change Current: ", dI)

            dV_ref = self.calc_perturb_amt(self.v_ref, v_in, i_in, t_in)
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
                print("[IC] Incremental Conductance: ", dC)
                if dI/dV*v_in == -i_in:
                    pass
                else:
                    if dI/dV*v_in > -i_in:
                        self.v_ref += dV_ref
                    else:
                        self.v_ref -= dV_ref

            # update values
            self.v_old = v_in
            self.i_old = i_in
            self.p_old = v_in*i_in

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