"""
Source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This file describes the Source class, which generates input values for the Display and MPPT.
"""

lookup_table = [
    [0.0,   5.8 ],
    [0.05,  5.8 ],
    [0.1,   5.8 ],
    [0.15,  5.8 ],
    [0.2,   5.8 ],
    [0.25,  5.8 ],
    [0.3,   5.8 ],
    [0.35,  5.8 ],
    [0.4,   5.8 ],
    [0.45,  5.8 ],
    [0.5,   5.8 ],
    [0.51,  5.8 ],
    [0.52,  5.8 ],
    [0.53,  5.8 ],
    [0.54,  5.7 ],
    [0.55,  5.6 ],
    [0.56,  5.5 ],
    [0.57,  5.3 ],
    [0.58,  5.05 ],
    [0.59,  4.8 ],
    [0.6,   4.6 ],
    [0.61,  4.0 ],
    [0.62,  3.0 ],
    [0.63,  2.1 ],
    [0.64,  1.2 ],
    [0.65,  1.0 ],
    [0.66,  0.3 ],
    [0.67,  0   ],
    [0.68,  0   ],
    [0.7,   0   ],
    [0.8,   0   ]
]
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
        closest_idx = 0
        idx = 0
        best_diff = 1000
        # basic linear search to find closest voltage. optimize later. swap to equation based model?
        for slice in lookup_table:
            # print("Looking at voltage: ", slice[0], " at idx: ", idx)
            diff = abs(v_in - slice[0])
            # print("Diff: ", diff)
            
            if diff < best_diff:
                # print("Best idx: ", closest_idx," is now updated to: ", idx)
                closest_idx = idx
                best_diff = diff
            else:
                break
            idx += 1

        self.i_out = lookup_table[closest_idx][1]
        # print("Current at nearest voltage: ", lookup_table[closest_idx][1])
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
