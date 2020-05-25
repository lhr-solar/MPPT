"""
mppt_incremental_conduction.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/25/20
Last Modified: 5/25/20
Description: Incremental Conduction Algorithm.
"""

class IC:
    v_ref = 0
    stride = 1
    sample_rate = 1

    p_old = 0
    v_old = 0
    i_old = 0

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
            # determine deltas
            dV = v_in - self.v_old
            dI = i_in - self.i_old

            print("Change Voltage: ", dV)
            print("Change Current: ", dI)

            dV_ref = .01 #dV # calc_perturb_amt(v_ref, v_in)
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