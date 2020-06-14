"""
Source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/28/20
Description: This file describes the Source class, which generates input values for the Display and MPPT.
    The Source is time agnostic. The output is purely dependent on current conditions.
"""
from math import exp, pow, e
from numpy import log as ln
class Source:
    irradiance  = 0
    temperature = 0
    load        = 0
    idx         = 0

    arr_cycle   = []
    arr_irrad   = []
    arr_temp    = []
    arr_load    = []

    model_type  = "Default"

    def __init__(self, model_type):
        """
        init
        Sets up the model type of the cell.

        Params:
            - model_type (String): type of model to represent the solar cell
                - [Benghanem]   (Considers Temperature but not Irradiance), default
                - Ibrahim       (Considers Temperature and Irradiance)
                - Zahedi        (Considers Temperature and Irradiance)
        
        Returns:
            - None
        """
        if model_type == "Benghanem":
            self.model_type = "Benghanem"
        elif model_type == "Ibrahim":
            self.model_type = "Ibrahim"
        elif model_type == "Zahedi":
            self.model_type = "Zahedi"
        else:
            self.model_type == "Default"

        return

    def setup_f(self, file_name=""):
        """
        setup_f (file) TODO:determine file structure, populate example file with data, and implement function to load it
        A data structure in the Source is populated from a file.

        Args:
            - file_name (string): file path to data file. A data file is formatted with the following types of values:
                - irradiance (W/m^2)
                - temperature (C)
                - load (W/s)

        Returns:
            - success (True) or failure (False) (bool)

        Note: efficiency losses are not considered (as of yet) in the Source model.
        """
        self.arr_cycle  = []
        self.arr_irrad  = []
        self.arr_temp   = []
        self.arr_load   = []
        return False
    
    def setup_a(self, regime):
        """
        setup_a (array)
        Populates Source data structure using an array of values.

        Args:
            - regime (list of lists): contains a list of events.
                - cycle | temp | TODO: NOT IMPLEMENTED

        Returns:
            - None
        """
        for event in regime:
            cycle = event[0]
            irrad = event[1]
            temp = event[2]
            load = 0
            
            self.arr_cycle.append(cycle)
            self.arr_irrad.append(irrad)
            self.arr_temp.append(temp)
            self.arr_load.append(load)

        print(self.arr_cycle)
        print(self.arr_temp)

    def setup_i(self, irradiance=0, temperature=0, load=0):
        """
        setup _i (impulse)
        Populates a data structure with user-set variables
        
        Args:
            - irradiance (float): light intensity on the cell (W/m^2)
            - temperature (float): surface temperature of the cell (C)
            - load (float): load on the system (W/s) NOTE: UNUSED

        Returns:
            - None

        Note: efficiency losses are not considered (as of yet) in the Source model.
        """
        self.irradiance = irradiance
        self.temperature = temperature
        self.load = load

    def iterate(self, v_in):
        """
        iterate
        Using source conditions, calculate the source voltage and current the system should expect.
        
        Args:
            - v_in (float): input voltage

        Returns:
            - (v_out, i_out) (tuple)
        """
        # NOTE: Defaulting to sunpower 1 cell at STD conditions
        v_out = v_in
        i_out = self.model(v_in, self.irradiance, self.temperature, self.load)
        return [v_out, i_out]

    def iterate_t(self, v_in, cycle):
        """
        iterate_t
        Using source conditions, calculate the source voltage and current the system should expect.
        NOTE: This version uses the cycle to pull relevant source conditions generated by setup(file_name).
        
        Args:
            - v_in    (float): input voltage
            - cycle   (int): cycle to grab source data from

        Returns:
            - [v_out, i_out, irrad, temp, load] (list)
        """
        # NOTE: Defaulting to sunpower 1 cell at STD conditions
        # try to set new conditions
        try:
            # if idx exists
            idx = self.arr_cycle.index(cycle)
            # load it
            v_out = v_in

            self.idx = idx
            self.irradiance = self.arr_irrad[idx]
            self.temperature = self.arr_temp[idx]
            self.load = self.arr_load[idx]
        except ValueError:
            print("[SOURCE] NOTE: Cycle does not exist in data. Interpolating data.")
            # if idx doesn't exist, grab two closest points
            idx_new = self.idx + 1
            idx_curr = self.idx
            try:
                # interpolate slope
                dCycle = (self.arr_cycle[idx_new] - self.arr_cycle[idx_curr])
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
                print("[SOURCE] NOTE: Cycle does not exist in data. Reached end of regime data. Don't interpolate.")
                insert_idx = idx_curr + 1
                self.arr_cycle.insert(insert_idx,   self.arr_cycle[insert_idx - 1] + 1)
                self.arr_irrad.insert(insert_idx,   self.arr_irrad[insert_idx - 1])
                self.arr_temp.insert(insert_idx,    self.arr_temp[insert_idx - 1])
                self.arr_load.insert(insert_idx,    self.arr_load[insert_idx - 1])
                
            return self.iterate_t(v_in, cycle)

        # model most recent conditions
        i_out = self.model(v_in, self.irradiance, self.temperature, self.load)
        return [v_out, i_out, self.irradiance, self.temperature, self.load]

    def get_conditions(self):
        """
        get_conditions
        Returns source conditions for data analysis.

        Args:
            - None

        Returns:
            - (irradiance, temperature, load) (tuple)

        """
        return [self.irradiance, self.temperature, self.load]

    def model(self, v_in, irr_in=0, t_in=0, ld_in=0):
        """
        model TODO: update with a more advanced model with irradiance
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
        if self.model_type == "Default":
            irr_ref = 1000
            i_sc = 6.15 # can be converted into a function of irradiance, temperature
            i_pv_ref = i_sc 
            # photovoltaic current
            r_sh = 0
            r_s = 0
            i_pv = i_pv_ref * irr_in / irr_ref

            # diode saturation current
            i_d = 4.1E-12 # this can be converted into a function of irradiance, temperature

            # output current
            q = 1.602E-19
            k = 1.381E-23 # in kelvin
            t_c = t_in + 273.15 # C to K
            model = i_pv - i_d * (exp(q*v_in/(k*t_c))-1)
            print("[SOURCE] Model: [I=", model, "|@V=", v_in, "IRR=", irr_in, "TEMP=", t_in, "LOAD=", ld_in, "]")

            # losses in efficiency as a result of manufacturing (lamination, etc)
            model2 = model * k
            
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

    def graph(self):
        """
        graph
        Returns an array of voltage and current values to display current solar panel IV pre-altered by the mppt.

        Args:
            - None

        Returns:
            - [[[voltage, current]], gmpp]
                - gmpp: global maximum power point characteristics, [vmpp, impp, pmpp]
        """
        MAX_VOLTAGE = 1
        v_in = 0
        step_size = .01
        p_mpp = 0
        v_mpp = 0
        i_mpp = 0
        output = []
        while True:
            [voltage, current] = self.iterate(v_in)
            output.append([voltage, current])
            if p_mpp < voltage * current:
                p_mpp = voltage * current
                v_mpp = voltage
                i_mpp = current

            v_in += step_size
            if current < 0 or voltage >= MAX_VOLTAGE:
                break
        return [output, [v_mpp, i_mpp, p_mpp]]
