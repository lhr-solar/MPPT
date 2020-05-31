"""
mppt.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/27/20
Last Modified: 5/28/20
Description: Parent class for various MPPT Algorithms.
    Algorithms Implemented: [x - implemented, u - considered, o - not considered]
        - [x] Perturb and Observe
        - [x] Incremental Conductance
        - [u] Ripple Correlation Control
        - [o] Fractional Open Circuit Voltage (it involves either pilot cells or the hutting down of the power converter, incurring power losses)
        - [o] Fractional Short Circuit Current (it involves an extra switch and sensor, and also causes power losses)
        - [u] Fuzzy Logic Control
        - [o] Current Sweep (causes loss of power, scanning for the mpp)
        - [x] dP/dV Feedback Control
    Ref:
        - Comparison of Photovoltaic Array Maximum Power Point Tracking Techniques (Esram et al)
"""
from math import log10
class MPPT:
    v_ref = 0
    stride = .1
    sample_rate = 1

    p_old = 0
    v_old = 0
    i_old = 0

    f_old  = 0
    dF_old = 0

    cycle_one = True

    stride_mode = ""

    def __init__(self):
        """
        init
        """
        return

    def setup(self, v_ref=0, stride=.1, sample_rate=1, stride_mode = "Piegari"):
        """
        setup
        Updates MPPT parameters
        
        Args:
            - v_ref (float): reference voltage (V)
            - stride (float): default fixed step.
            - sample_rate (int): cycles per iteration (1/Hz)

        Returns:
            - None
        """
        self.v_ref = v_ref
        self.stride = stride
        self.sample_rate = sample_rate
        self.stride_mode = stride_mode

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
        return self.v_ref

    def calc_perturb_amt(self, v_ref, v_in, i_in, t_in):
        """
        calc_perturb_amt
        Uses a black box method to determine the change to v_ref

        Args:
            - v_ref (float): output reference voltage
            - v_in  (float): source voltage
            - i_in  (float): source current
            - t_in  (float): temperature

        Returns:
            - dV_ref (float): change in new reference voltage for current iteration

        Ref:
            1. Optimized Adaptive Perturb and Observe Maximum Power Point Tracking Control for Photovoltaic Generation (Piegari et al.)
                - Section 3, Adaptive Perturbation Function for P&O Algorithm
                - dV = f(V_best-V) + dV_min
                - f(V_best-V) = |V_best - V| optimally
                - V_best unlikely to match physical conditions, need to add an error estimation
                    - dV_min > k^2/(2*(1-k))*V
                    - k = .05 - 5% error
                - Can also optimize V_best based on temperature
                    - plotting voltage at max power from the source model, we can use a best polynomial fit
                        - 8.93*.000001*(t_in**2) -4.04*.001*t_in + .717
        """

        if self.stride_mode == "Piegari":
            k = .05 # 5 percent error
            v_best = .621 # according to Sunniva
            v_best = 8.93*.000001*t_in*t_in -4.04*.001*t_in + .717
            print("v_best=", v_best, "@T=", t_in)
            dV_min = .5*(k*k)/(1-k)*v_in + .001
            stride = abs(v_best - v_in)
            print("f(V_best-V) = ", stride)
            print("dV_min = ", dV_min)
            if stride < dV_min:
                return stride
            else:
                return (stride + dV_min)
        elif self.stride_mode == "Newton":
            # newton's method
            """
            Newton's method seeks to find min f(X).
            In this case, f(x) = transformed P-V curve, which is 0 at vmpp.
            Ideally, the transfomed PV curve is of the form f(V)= -P(V) + Pmpp.
            Pmpp has to be estimated, or some error checking should be performed.

            Our initial guess is v_ref.
            """
            p_mpp = 3.62 # Wp, according to sunniva
            # pveducation says that Voc and Isc is a good approx of Vmp and Imp
            # v_mpp = v_oc = .721 - (2.2*.001)*(t_in-25)
            # i_mpp = i_sc = 6.15 + (.06*.001)*(t_in-25)*6.15
            # k = .8186 # in this case, p_mpp is 3.63 but oc*ssc is 4.43 so we need a constant to regulate it
            # p_mpp = v_mpp * i_mpp * k

            f = 0
            dF = 0
            # need two points to determine slope, check if I'm on the first step
            if self.cycle_one:
                self.cycle_one = False
                f = -v_in*i_in + p_mpp
                dF = 0
            else:
                f = -v_in*i_in + p_mpp
                print("f = ", f)

                diff_v = v_in - self.v_old
                print("diff_v:", diff_v)
                diff_f = f - self.f_old
                print("diff_f:", diff_f)

                if diff_v == 0: # we've found the mpp
                    self.stride = 0
                    dF = 0
                else:
                    dF = diff_f/diff_v
                    print("dF:", dF)
                    if dF == 0: # also found the mpp
                        self.stride = 0
                    else:
                        self.stride = abs(- f/dF)
                        print("v_ref:", self.stride)

            self.f_old = f
            self.dF_old= dF 
            return self.stride

        elif self.stride_mode == "LBFGS":
            return .1
        else:
            return self.stride


    def get_name(self):
        """
        get_name
        Returns mppt algorithm name.
        
        Args:
            - None

        Returns:
            - Name (String)
        """
        return ""