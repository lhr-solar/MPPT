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
class MPPT:
    v_ref = 0
    stride = .1
    sample_rate = 1

    p_old = 0
    v_old = 0
    i_old = 0

    f_old  = 0
    dF_old = 0

    # for Ternary and Golden
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

    def setup(self, v_ref=0, stride=.1, sample_rate=1, stride_mode = "Fixed"):
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
        if self.stride_mode == "Fixed": # mode 1
            return self.stride
        elif self.stride_mode == "Ternary":
            """
            Ternary Search
            https://en.wikipedia.org/wiki/Ternary_search

            Ternary search seeks to find the min/max of a unimodal function.
            In this case, f(x) = P-V curve, which is at max at vmpp.

            Does not require an initial guess, but assumes that the initial voltage bound is [0, .8].
            """
            [left, right] = self.bounds
            cycle = self.cycle

            # Ternary - we need points every iteration: left third and right third
            if cycle == 0: # set left third
                self.l2_pow = v_in * i_in
                # restrict the bounds           - this works in the base case since l1 and l2 is initialized to bounds
                if self.l1_pow > self.l2_pow:
                    self.bounds[1] = self.l2
                else:
                    self.bounds[0] = self.l1
                # calculate l1 to test
                self.l1 = (right-left)/3 + left                
                self.stride = self.l1
                self.cycle += 1
            elif cycle == 1: # set right third
                self.l1_pow = v_in * i_in
                # calculate l2 to test
                self.l2 = right - (right-left)/3
                self.stride = self.l2
                self.cycle = 0
            else:
                print("[ERROR] I shouldn't be here.")

            return self.stride
        elif self.stride_mode == "Golden":
            """
            Golden Section Search
            https://en.wikipedia.org/wiki/Golden-section_search

            Golden Section search seeks to find the min/max of a unimodal function.
            In this case, f(x) = P-V curve, which is at max at vmpp.

            Does not require an initial guess, but assumes that the initial voltage bound is [0, .8].
            """
            [l, r] = self.bounds
            cycle = self.cycle

            if cycle == 0:
                # find l1
                self.l1 = r-(r-l)*self.phi
                self.stride = self.l1
                self.cycle += 1
            elif cycle == 1:
                # find l2
                self.l1_pow = i_in*v_in
                self.l2 = (r-l)*self.phi+l
                self.stride = self.l2
                self.cycle += 1
            else:
                if cycle == 2: # updated l2 in previous round
                    self.l2_pow = i_in*v_in
                elif cycle == 3: # updated l1 in previous round
                    self.l1_pow = i_in*v_in
                else:
                    print("[ERROR] I shouldn't be here.")

                # compare and cut the bounds
                if self.l1_pow > self.l2_pow:
                    # cut right side
                    self.bounds[1] = self.l2
                    # l1 becomes l2
                    self.l2 = self.l1
                    self.l2_pow = self.l1_pow
                    # find next l1
                    [l, r] = self.bounds
                    self.l1 = r-(r-l)*self.phi
                    self.stride = self.l1
                    self.cycle = 3
                else:
                    # cut left side
                    self.bounds[0] = self.l1
                    # l2 becomes l1
                    self.l1 = self.l2
                    self.l1_pow = self.l2_pow
                    # find next x1
                    [l, r] = self.bounds
                    self.l2 = (r-l)*self.phi+l
                    self.stride = self.l2
                    self.cycle = 2

            return self.stride
        elif self.stride_mode == "Optimal":
            # Piegari - we assume we know where the mpp should be and jump to there
            k = .05 # 5 percent error
            v_mpp = .47282#.621 # according to Sunniva # TODO UPDATE THIS ESTIMATE
            v_min = k*k/(2*(1-k))*v_mpp + .001
            stride = abs(v_mpp - v_in)
            return stride + v_min
        elif self.stride_mode == "Newton":
            """
            Newton's method.

            Newton's method seeks to find min f(X).
            In this case, f(x) = transformed P-V curve, which is 0 at vmpp.
            Ideally, the transfomed PV curve is of the form f(V)= -P(V) + Pmpp.
            Pmpp has to be estimated, or some error checking should be performed.

            Our initial guess is v_ref.
            """
            # p_mpp = 3.62 # pmpp, according to sunniva
            k = .995 # error approximation to get p_mpp always below P(vmpp)
            p_mpp = (4.32 + -.0293*t_in + 6.4E-05*(t_in**2)) * k

            # need two points to determine slope, check if I'm on the first step
            if self.cycle_one:
                self.cycle_one = False
                self.f_old = -v_in*i_in + p_mpp
                # v_old is set outside this in the parent
                self.dF_old = 0
            else:
                f = -v_in*i_in + p_mpp
                # print("[MPPT] f:", f)

                diff_v = v_in - self.v_old
                # print("[MPPT] diff_v:", diff_v)
                diff_f = f - self.f_old
                # print("[MPPT] diff_f:", diff_f)

                if diff_v == 0: # we've found the mpp
                    self.stride = v_in + 0
                    dF = 0
                else:
                    dF = diff_f/diff_v
                    # print("[MPPT] dF:", dF)
                    if dF == 0: # slope is 0, MPP is in the middle
                        self.stride = v_in + diff_v/2
                    else:
                        self.stride = v_in - f/dF
                        # print("[MPPT] v_ref:", self.stride)

                self.f_old = f
                self.dF_old= dF 
            if(self.stride > .8 or self.stride < 0):
                self.stride = 0
                print("Warning, Newton output has exceeded range", self.stride)
            return self.stride
        elif self.stride_mode == "BFGS": #LBFGS
            return self.stride
        else: # default Fixed
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