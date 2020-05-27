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
        """
        if (cycle % self.sample_rate) is 0:
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

    def calc_perturb_amt(self, v_ref, v_in, t_in):
        """
        calc_perturb_amt
        Uses a black box method to determine the change to v_ref

        Args:
            - v_ref (float): output reference voltage
            - v_in (float): source voltage
            - t_in  (float): temperature
        Returns:
            - dV_ref (float): change in new reference voltage for current iteration
        NOTE: BLACK BOX THIS and swap out new methods
        """
        # function 1: dV = f(V_best-V) + dV_min
        # Optimized Adaptive Perturb and Observe Maximum Power Point Tracking Control for Photovoltaic Generation
        # Piegari et al.
        # f(V_best-V) would optimally be |V_best - V|
        # but the V_best is unlikely to match physical conditions, so we need to add an error estimation
        # propose that dV_min > k^2/(2*(1-k))*V
        # return .005

        k = .05 # 5 percent error
        v_best = .621 # according to Sunniva
        # we can optimize v_best based on temp. Plotting the voltage at max power from the source model equation, we can use a primitive best polynomial line fit.
        v_best = 8.93*.000001*t_in*t_in -4.04*.001*t_in + .717
        print("v_best=", v_best, "@T=", t_in)
        dV_min = .5*(k*k)/(1-k)*v_in + .001
        x = abs(v_best - v_in)
        print("f(V_best-V) = ", abs(v_best - v_in))
        print("dV_min = ", dV_min)
        if x < dV_min:
            return x
        else:
            return x + dV_min