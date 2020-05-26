"""
Source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This file describes the Source class, which generates input values for the Display and MPPT.
"""
from math import exp
from numpy import log as ln
class Source:
    cycle = 0
    time_step = 1
    v_out = 0
    i_out = 0
    irradiance = 0
    temperature = 0
    load = 0

    def __init__(self):
        """
        init
        """
        return

    def read_data(self, file_name=""):
        """
        read_data 
        A data structure in the Source is populated from a file.

        Args:
            - file_name (string): file path to data file. A data file is formatted with the following types of values:
                - irradiance (W/m^2)
                - temperature (C)
                - load (W/s)
        Returns:
            - None
        Note: efficiency losses are not considered (as of yet) in the Source model.
        """
        return

    def read_data(self, irradiance=0, temperature=0, load=0):
        """
        read_data 
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

    def setup(self, cycle, time_step):
        """
        setup
        Updates source parameters

        Args:
            - cycle (int): new start cycle of the source
            - time_step (int): change in cycles every program iteration NOTE: UNUSED
        Returns:
            - None
        """
        self.cycle = cycle
        self.time_step = time_step

    def iterate(self, v_in):
        """
        iterate
        Using a source conditions, calculate the source voltage and current the system should expect.
        
        Args:
            - v_in (float): input voltage
        Returns:
            - (v_out, i_out, cycle) (tuple)
        """
        # TODO: using current timestep, load appropriate inputs and convert to v_out, i_out.
        # NOTE: Defaulting to sunpower 8 cell module at STD conditions

        # print("Input voltage: ", v_in)
        # print("Looking for closest voltage.")

        self.v_out = v_in

        self.i_out = self.model(v_in)
        # print("Current at voltage: ",  model(v_in))
        self.cycle += 1
        return [self.v_out, self.i_out, self.cycle]

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

    def model(self, v_in):
        """
        model
        function describing the current output of a single Bin Le1 Sunpower cell given voltage and other factors.
        Taken from https://www.sciencedirect.com/science/article/pii/S1658365512600120, section 2.1, Explicit Model.
        Im/Vm constants played with until they matched cell specs for the power point.
        
        model(v) = 6.15*( 1 - C_1*( exp( v/(C_2*.721) ) - 1 ) )
        C_1 = (1 - C_4/.721)*exp( -C_3/(C_2*.721) )
        C_2 = ((C_3/.721) - 1) / ln(1 - C_4/6.15)

        6.15 - I_SC
        .721 - V_OC

        C_3 = maximal voltage
        C_4 = maximal current

        TODO: include inputs for irradiance, temperature, and their transformation on the model

        Args:
            - v_in (float): voltage input
        Returns:
            - (current out) (float)
        """
        k = 0.92 # manufacturing efficiency loss (8% according to test data)
        C_3 = 0.82 # maximal voltage
        C_4 = -100 # maximal current
        C_2 = ((C_3/.721) - 1) / ln(1 - C_4/6.15)
        C_1 = (1 - C_4/.721)*exp( -C_3/(C_2*.721) )
        # default explicit model
        model = 6.15*( 1 - C_1*( exp( v_in/(C_2*.721) ) - 1 ) )

        # losses in efficiency as a result of manufacturing (lamination, etc)
        model2 = model * k

        # TODO: include transformation for irradiance change, temperature
        return model2
    
