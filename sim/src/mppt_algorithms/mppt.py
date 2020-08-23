"""
mppt.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/27/20
Last Modified: 6/24/20
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
from math import log10, sqrt
from math import exp
class MPPT:
    v_ref = 0
    stride = .1
    sample_rate = 1

    p_old = 0
    v_old = 0
    i_old = 0

    f_old  = 0
    dF_old = 0

    # for Ternary, Golden, Bisection
    cycle = 0
    bounds = [0, .8]
    l1 = bounds[0]
    l1_pow = 0
    l2 = bounds[1]
    l2_pow = 0
    phi = (sqrt(5) + 1)/2 - 1

    cycle_one = True

    stride_mode = ""

    def __init__(self):
        """
        init
        """
        return

    def setup(self, v_ref=0, stride=.1, sample_rate=1, stride_mode=None):
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
        if stride_mode is None:
            stride_mode = "Fixed"
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
                    - dV_min > k^2/(2*(1-k))*V_best
                    - k = .05 - 5% error
                - Can also optimize V_best based on temperature
                    - plotting voltage at max power from the source model, we can use a best polynomial fit
                        - .717 + -4.04E-03t + 8.93E-06t^2
            2. Novel algorithm of MPPT for PV array based on variable step Newton-Raphson method through model predictive control (Hosseini et al.)
                - Section 3.2, Maximum Power Point Tracker of Variable Step
                - v_ref = v_in - F(v_in)/F'(v_in)
                - stride= -F(v_in)/F'(v_in)
                - F(v_in) needs to be a function with a 0 at the max power point
                    - let F(v_in) = - P(v_in) + pmpp
                    - pmpp is going to be variable based on irradiance and temp
                        - it needs to fulfil the condition P(vmpp) > pmpp, otherwise things break
                        - our approximation needs to be GOOD
                - analytically, F'(v_in) is the slope of F(v_in) - we need two points (can't use instant. ROC)
                    - F'(v_in) = (F(v_in) - F(v_old)) / (v_in - v_old)
                - Can optimize pmpp based on temperature
                    - plotting Source Model 1's pmpp across temperature, a 2nd order polynomial fit line is obtained
                        - 4.32 + -.0293t + 6.4E-05t^2
        """
        v_mpp = .47282 # .621 # according to Sunniva # TODO UPDATE THIS ESTIMATE
        if self.stride_mode == "Optimal":
            # Piegari - we assume we know where the mpp should be and jump to there
            k = .1 # 10% estimation error
            v_min = k*k/(2*(1-k))*v_mpp # this works out to be .55% for a 10% estimation error
            
            stride = abs(v_mpp - v_in)
            return stride + v_min
        elif self.stride_mode == "Adaptive":
            # Piegari - we assume we know where the mpp should be and use the following piecewise function
            # f(V_M - V) = (exp(V_M - V)/3 - 1) V < V_M
            #              0                    V > V_M
            k = .2 # 20% estimation error
            v_min = k*k/(2*(1-k))*v_mpp
            
            if v_in < v_mpp:
                stride = exp((v_mpp - v_in)/3)-1 + v_min
            else:
                stride = v_min
            return stride
        else: # default fixed
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