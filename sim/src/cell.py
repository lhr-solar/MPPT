"""
Cell.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 8/9/20
Last Modified: 8/9/20

Description: This file describes the Cell class, which generates a model for the
Source class based on environmental inputs. The Cell is time agnostic. The
output is purely dependent on current conditions.

Functionality: I should be able to do the following:
    - (setup) load from a configuration file or pass in an impulse or regime
        (the latter two are for single cell source modelling). 
    - (iterate) able to step forward a cycle and return PV voltage and current. 
        Depends on model. 
    - (model) able to return the current given a model type and the environmental
        conditions (voltage applied, irradiance, temp, load) 
    - (get_cell_IV) able to get the IV curve of the PV at the current cycle. Depends 
        on model and runs a scan using voltage applied. 
    - (get_cell_gmpp) able to get the GMPP characteristics of the PV at the 
        current cycle. Depends on model and runs a scan using voltage applied. 
    - (get_env_conditions) able to get the environmental conditions for the cell 
        for the current cycle. 
    - (get_model_type) able to get the current cell model name (i.e. nonideal,
        ideal). 
    - (set_current_cycle, increment_cycle) able to jump forward and
        rewind back in time.
"""
from math import exp, pow, e
from numpy import log as ln

from src.source_file import SourceFile
class Cell:
    MAX_VOLTAGE = .8
    setup_type = ""

    irradiance  = 0
    temperature = 0
    load        = 0
    idx         = 0
    cycle       = 0

    arr_cycle   = []
    arr_irrad   = []
    arr_temp    = []
    arr_load    = []

    model_type  = "Default"

    use_file = False
    source_file = None

    def __init__(self, model_type="Default", use_file=True):
        """
        init
        Sets up the model type of the cell.

        Params:
            - model_type (String): type of model to represent the solar cell
                - [Nonideal]    (Single diode nonideal cell), default
                - Ideal         (Single diode ideal cell)
            - use_file (bool): use source_file if true.
        
        Returns:
            - None
        """
        if model_type == "Ideal":
            self.model_type = "Ideal"
        else:
            self.model_type = "Nonideal"
        
        if use_file:
            self.source_file = SourceFile()
            self.source_file.read_file()
            self.use_file = True

    def setup(self, setup_type="", regime=[], impulse=()):
        """
        setup Sets up an internal environmental regime either using an array of
        values, a file, or with initial conditions (an impulse).

        Args:
            - self
            - type      (String): Either "Array", or "Impulse".
            - regime    ([[(int) Cycle, (float) Irradiance, (float) Temperature], ...]): Environmental regime.
            - impulse   (((float) Irradiance, (float) Temperature)): Impulse

        Return:
            - Whether the setup was successful (bool)

        Notes:
            - irradiance (float): light intensity on the cell (W/m^2)
            - temperature (float): surface temperature of the cell (C)
            - load (float): load on the system (W/s) NOTE: UNUSED

        # TODO: no support for load at the moment.
        """
        # refresh values
        self.arr_cycle  = []
        self.arr_irrad  = []
        self.arr_temp   = []
        self.arr_load   = []
        irradiance      = 0
        temperature     = 0
        load            = 0
        self.idx        = 0
        self.cycle      = 0

        if setup_type == "":
            print("[CELL] WARN: Empty setup type -", setup_type)
            return False

        elif setup_type == "Array":
            if not regime:
                print("[CELL] WARN: Array setup type was selected, but regime is an empty list.")
                return False

            for event in regime:
                self.arr_cycle.append(event[0])
                self.arr_irrad.append(event[1])
                self.arr_temp.append(event[2])
                self.arr_load.append(0)
            
            self.setup_type = "Array"
            self.cycle = 0
            return True

        elif setup_type == "Impulse":
            if not impulse:
                print("[CELL] WARN: Impulse setup type was selected, but impulse is an empty tuple.")
                return False

            self.irradiance = impulse[0]
            self.temperature = impulse[1]
            self.load = 0

            self.setup_type = "Impulse"
            self.cycle = 0
            return True

        else:
            print("[CELL] WARN: Invalid setup type -", setup_type)
            return False

    def iterate(self, v_in):
        """
        iterate Using source conditions, calculate the source voltage and
        current the system should expect. If done in impulse mode, we take the
        current conditions, but if done in array mode, we take the passed in
        cycle and interpolate from the regime.

        Args:
            - v_in    (float): input voltage
            - cycle   (int): cycle to grab source data from

        Returns:
            - (v_out, i_out, irrad, temp, load) (tuple)

        NOTE: This model is for Sunpower 1 cell at STD conditions
        NOTE: the cycle needs to be manually incremented after calling iterate.
        """
        if self.setup_type == "Impulse":
            v_out = v_in
            i_out = self.model(v_in, self.irradiance, self.temperature, self.load)
            return (v_out, i_out, self.irradiance, self.temperature, self.load)

        elif self.setup_type == "Array":
            # try to set new conditions
            v_out = v_in
            try:
                # if idx exists
                idx = self.arr_cycle.index(self.cycle)

                self.idx = idx
                self.irradiance = self.arr_irrad[idx]
                self.temperature = self.arr_temp[idx]
                self.load = self.arr_load[idx]
            except ValueError:
                print("[CELL] NOTE: Cycle ", self.cycle, " does not exist in data. Interpolating data.")
                # if idx doesn't exist, grab two closest points
                idx_new = self.idx + 1
                idx_curr = self.idx
                try:
                    # interpolate slope
                    dCycle = (self.arr_cycle[idx_new] - self.arr_cycle[idx_curr])
                    # round if we can
                    sIrr   = (self.arr_irrad[idx_new] - self.arr_irrad[idx_curr])/dCycle
                    sTemp  = (self.arr_temp[idx_new] - self.arr_temp[idx_curr])/dCycle
                    sLoad  = (self.arr_load[idx_new] - self.arr_load[idx_curr])/dCycle

                    for i in range(0, dCycle - 1): # append entries to relevant arrays
                        insert_idx = idx_curr + i + 1
                        self.arr_cycle.insert(insert_idx,   self.arr_cycle[insert_idx - 1] + 1)
                        self.arr_irrad.insert(insert_idx,   self.arr_irrad[insert_idx - 1] + sIrr)
                        self.arr_temp.insert(insert_idx,    self.arr_temp[insert_idx - 1] + sTemp)
                        self.arr_load.insert(insert_idx,    self.arr_load[insert_idx - 1] + sLoad)
                except IndexError:
                    print("[CELL] NOTE: Cycle ", self.cycle, " does not exist in data. Reached end of regime data. Don't interpolate.")
                    insert_idx = idx_curr + 1
                    self.arr_cycle.insert(insert_idx,   self.arr_cycle[insert_idx - 1] + 1)
                    self.arr_irrad.insert(insert_idx,   self.arr_irrad[insert_idx - 1])
                    self.arr_temp.insert(insert_idx,    self.arr_temp[insert_idx - 1])
                    self.arr_load.insert(insert_idx,    self.arr_load[insert_idx - 1])
                finally:
                    # now get the result after we've interpolated it
                    return self.iterate(v_in)
            finally:
                # model most recent conditions
                i_out = self.model(v_in, self.irradiance, self.temperature, self.load)
                return (v_out, i_out, self.irradiance, self.temperature, self.load)

        else:
            print("[CELL] WARN: Invalid setup type -", setup_type)
            # return not useful, identifiable data. TODO: Maybe throw an exception.
            return (0, 0, 0, 0, 0)

    def model(self, v_in, irr_in=0.001, t_in=0, ld_in=0):
        """
        model
        Function describing the current output of a SINGLE Bin Le1 Sunpower cell given voltage and other factors.
    
        Args:
            - v_in      (float): voltage input      (V)
            - irr_in    (float): irradiance input   (W/m^2)
            - t_in      (float): temperature input  (C)
            - ld_in     (float): load input         (W)

        Returns:
            - (current out) (float)

        Ref:
            1. Modeling of photovoltaic module and experimental determination of serial resistance (Benghanem et Alamri)
                - Section 2.1, Explicit Model        
                - model(v) = i_sc*( 1 - C_1*( exp( v/(C_2*v_oc) ) - 1 ) )
                    ~ C_1 = (1 - C_4/i_sc)*exp( -C_3/(C_2*v_oc) )
                    ~ C_2 = ((C_3/v_oc) - 1) / ln(1 - C_4/i_sc)
                    ~ https://www.pveducation.org/pvcdrom/solar-cell-operation/effect-of-temperature
                        - for silicon solar cell
                        - V_OC = .721 - (2.2*.001)*(t-25)
                        - I_SC = 6.15 + .0006*(t-25)*6.15
                    ~ C_3 = maximal voltage
                    ~ C_4 = maximal current
            2. Modeling and simulation of photovoltaic arrays (Banu et Istrate)
                - Section 2, Simulink Model of Solar Cell
                - TODO: Implement this?
            3. Review of modelling details in relation to low-concentration solar cell concentrating photovoltaic (Zahedi)
                - Section 3-6
                - G - irradiance, W/m^2

                - I = I_L(G, T_c) - I_D(V, G, T_c)
                    - load current is a result of light generated current and diode saturation current
                - I_L(G, T_c) = I_SC(G, T_c)
                    - light generated current is equal to the short circuit current in an ideal cell
                - I_SC(G, T_c) = I_SC,ref * (1 + K_t * (T_c-T_ref) * G / Gref
                    ~ I_SC,ref = reference short circuit current (A)
                        - 6.15 A
                    ~ K_t = some constant
                        - 0 for I_SC to be ideal
                    ~ T_c = T_a + (NOCT-20)/80 * S 
                        - https://www.pveducation.org/pvcdrom/modules-and-arrays/nominal-operating-cell-temperature
                        - T_a = ambient air temp (C)
                            ~ avg low to high in Austin from June to Aug is 72-97 F (22.2-36C)
                        - NOCT = cell temp at NOCT (C)
                            ~ going with typical module NOCT of 48C, sunniva STD was at 25C, no other details
                        - S = insolation (incident solar radiation)
                            ~ 1000 W/m^2 -> 100 mW/cm^2 during the summer solstice in Austin, Energy, the Environment, and Sustainability (2018) p. 213 [Efstathios E. Michaelides]
                    ~ T_ref = reference temperature (C)
                        - 25 C
                    ~ G = solar irradiance (W/m^2)
                        - variable
                    ~ G_ref = reference solar irradiance (W/m^2)
                        - 1000 W/m^2
                - I_D = I_SC/(exp(V_OC * (1 + K_v * (T_c-T_ref)) / (a * V_T)) - 1)
                    ~ I_SC = short circuit current, see above (A)
                    ~ V_OC = open circuit voltage (V)
                        - doesn't say reference, but assume it is or we're missing things
                        - .721 V
                    ~ K_v = some constant
                        - -.00023 fixed by the paper, NOTE: it can be tweaked
                    ~ a = diode ideality factor (1-1.5)
                        - 1.187, NOTE: can be tweaked
                    ~ V_T - thermal voltage (V)
                        - V_T = k * T_c / q
                            - k = boltzmann's constant
                                ~ 1.381 * 10^-23 J/K
                            - T_c = cell temperature, see above (in Kelvin -> f(C) = C + 273.15)
                            - q = electron charge
                                ~ 1.602 * 10^-19 C
        """
        if self.use_file and self.model_type == "Nonideal":
            return(float(self.source_file.retrieve_source([round(v_in, 2), irr_in, t_in])))
        else:
            threshold = .005

            k       = 1.381E-23
            q       = 1.602E-19
            t_ref   = 25+273.15
            irr_ref = 1000
            v_oc_ref= .721
            i_sc_ref= 6.15
            r_s     = .032
            r_sh    = 36.1

            # overflow error if irr_in is 0
            if irr_in == 0:
                irr_in = .001

            if self.model_type == "Default" or self.model_type == "Nonideal":
                # convert t_in from C to K
                t_c = t_in + 273.15

                # nonideal single diode model
                i_sc = irr_in / irr_ref * i_sc_ref * (1 + 6E-4 * (t_c - t_ref))
                v_oc = v_oc_ref - 2.2E-3 * (t_c - t_ref) + k * t_c / q * ln(irr_in / irr_ref)
                i_pv = i_sc
                i_0  = exp(ln(i_sc) - q * v_oc / (k * t_c))

                # iteratively solve implicit parameter
                i = 0
                left = i

                right = i_pv - i_0 * (exp(q * (v_in + i * r_s) / (k * t_c)) - 1) - (v_in + i * r_s) / r_sh
                difference = (left - right) * (left - right)
                decreasing = True

                while decreasing:
                    i = i + .001
                    left = i
                    right = i_pv - i_0 * (exp(q * (v_in + i * r_s) / (k * t_c)) - 1) - (v_in + i * r_s) / r_sh
                    if (difference - (left - right) * (left - right)) <= 0.0: # positive
                        decreasing = False
                    difference = (left - right) * (left - right)

                model = i
                # print("[SOURCE] Model: [I=", model, "|@V=", v_in, "IRR=", irr_in, "TEMP=", t_c, "LOAD=", ld_in, "]")
                # losses in efficiency as a result of manufacturing (lamination, etc)
                # model2 = model * k
                return model

            if self.model_type == "Ideal":
                # ideal single diode model
                t_c = t_in + 273.15 # convert into kelvin

                i_sc = irr_in / irr_ref * i_sc_ref * (1 + 6E-4 * (t_c - t_ref))
                v_oc = v_oc_ref - 2.2E-3 * (t_c - t_ref) + k * t_c / q * ln(irr_in / irr_ref)
                i_pv = i_sc
                i_0 = exp(ln(i_sc) - q * v_oc / (k * t_c))
                i_d = i_0 * (exp(q * v_in / (k * t_c) - 1))
                i = i_pv - i_d

                model = i
                # print("[SOURCE] Model: [I=", model, "|@V=", v_in, "IRR=", irr_in, "TEMP=", t_c, "LOAD=", ld_in, "]")
                # losses in efficiency as a result of manufacturing (lamination, etc)
                # model2 = model * k
                return model

            if self.model_type == "Benghanem":
                k = 0.92 # manufacturing efficiency loss (8% according to test data)

                # open circuit voltage and short circuit current dependence on temperature
                v_oc = .721 - (2.2*.001)*(t_in-25)
                i_sc = 6.15 + (.06*.001)*(t_in-25)*6.15

                C_3 = 0.817 # maximal voltage - determined by tuning parameters in desmos until maxppt is reached
                C_4 = -100  # maximal current

                C_2 = ((C_3/v_oc) - 1) / ln(1 - C_4/i_sc)
                C_1 = (1 - C_4/i_sc)*exp( -C_3/(C_2*v_oc) )
                # default explicit model
                model = i_sc*( 1 - C_1*( exp( v_in/(C_2*v_oc) ) - 1 ) )
                print("[SOURCE] Model: [I=", model, "|@V=", v_in, "IRR=", irr_in, "TEMP=", t_in, "LOAD=", ld_in, "]")

                # losses in efficiency as a result of manufacturing (lamination, etc)
                model2 = model * k
                
                return model
            
            if self.model_type == "Ibrahim":
                return 0

            if self.model_type == "Zahedi":
                # TODO: Severe issues, not yet usable. Continue to debug.
                k = 0.92 # manufacturing efficiency loss (8% according to test data)

                G = irr_in
                T_a = 36
                # ignore T_c equation and insert our own cell temp into it
                T_c = t_in # T_a + (48 - 20) / 80 * 100 
                I_sc= 6.15 * (1 + 0 * (T_c - 25)) * G / 1000
                print("[SOURCE] Short Circuit current I_sc:", I_sc)

                I_l = I_sc
                K_v = -.00023
                a = 1.187
                V_t = 1.381E-23 * (T_c + 273.15) / 1.602E-19
                print("[SOURCE] Thermal voltage V_t:", V_t)
                I_d = I_sc / (exp(.721 * (1 + K_v * (T_c - 25)) / (a * V_t)) - 1) * (e ** (v_in / (a * V_t)) - 1)
                print("[SOURCE] denom:", (exp(.721 * (1 + K_v * (T_c - 25)) / (a * V_t)) - 1))
                print("[SOURCE] multiplier:", (e ** (v_in / (a * V_t)) - 1))
                print("[SOURCE] Diode Saturation current:", I_d)
                model = I_l - I_d
                print("[SOURCE] Model: [I=", model, "|@V=", v_in, "IRR=", irr_in, "TEMP=", t_in, "LOAD=", ld_in, "]")

                # losses in efficiency as a result of manufacturing (lamination, etc)
                model2 = model * k 
                return model

    def get_cell_IV(self, step_size=.01):
        """
        get_cell_IV 
        Returns an array of PV characteristics of the cell at the current environmental conditions.

        Args: 
            - step_size (float): step size. Defaults to .01 V.

        Returns: 
            - [[[voltage, current], ...], gmpp] 
                - gmpp: global maximum power point characteristics, vmpp, impp, pmpp]
        """
        v_in = 0
        p_mpp = 0
        v_mpp = 0
        i_mpp = 0
        output = []

        while True:
            (voltage, current, _irradiance, _temp, _load) = self.iterate(v_in)
            output.append([voltage, current])
            if p_mpp < voltage * current:
                p_mpp = voltage * current
                v_mpp = voltage
                i_mpp = current

            v_in += step_size
            if round(v_in, 4) > self.MAX_VOLTAGE: # round to prevent E-5 float being larger than self.MAX_VOLTAGE
                break


        return [output, [v_mpp, i_mpp, p_mpp]]

    def get_cell_gmpp(self):
        """
        get_cell_gmpp 
        Returns the global maximum power point parameters to be
        used by the simulation display. Uses ternary search to find the maximum
        of the unimodal single cell. This will not work for a multi module
        model.

        Returns: 
            - (vmpp, impp, pmpp) tuple of global maximum power point characteristics
        """
        [output, [v_mpp, i_mpp, p_mpp]] = self.get_cell_IV()
        return (v_mpp, i_mpp, p_mpp)

    def get_env_conditions(self):
        """
        get_env_conditions
        Returns cell conditions for the most recent cycle for data analysis.

        Args:
            - None

        Returns:
            - (irradiance, temperature, load) (tuple)
        """
        return (self.irradiance, self.temperature, self.load)

    def get_model_type(self):
        """
        get_model_name
        Returns the name of the model.

        Args:
            - None
        Returns:
            - String name
        """
        return self.model_type

    def set_current_cycle(self, cycle):
        """
        set_current_cycle 
        Sets the current cycle for all modules in the PV.

        Args:
            - cycle (int): current cycle for the PV modules.
        """
        self.cycle = cycle

    def increment_cycle(self):
        """
        increment_cycle 
        Increments the current cycle for the cell

        Returns:
            current cycle.
        """
        self.cycle += 1
        return self.cycle