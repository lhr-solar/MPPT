"""
source_file.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 8/15/20
Last Modified: 8/16/20

Description: This file is a standalone file that can be inserted into a program to read and write
    an encoded model from a .csv. This speeds up model calculations.

    Generates a high fidelity model of the source and encodes it into a csv file. This can be used 
    by other programs to quickly grab data given a keyed set of independent conditions.
    
    The file is organized into the following columns:
        v_ref, irradiance, temperature, current
        Every entry should be unique.

    The file is sorted in increasing order by leftmost column priority.
        That is:
        v   |   irr |   temp|   current
        ---------------------------------------
        0   ,   0   ,   0   ,   X
        0   ,   0   ,   0   ,   X
        0   ,   0   ,   0.1 ,   X
        0   ,   0   ,   0.2 ,   X
        0   ,   1.0 ,   10  ,   X
        0   ,   1.0 ,   12  ,   X
        0   ,   1.0 ,   15  ,   X
        ... and so on.

    We can ignore sorting and insertion if we insert in order with a clever source building scheme.
    Retrieval can then be reduced to an indexing scheme that is O(1).

    We can also eliminate the need to interpolate data if we clearly define the minimum resolution
    across each independent variable.
"""
import csv
import time

CELL_MODEL_HEADER = "cell_1"

class SourceFile():
    header = []
    data = []
    file = ""

    def __init__(self, header=CELL_MODEL_HEADER, file="model.csv"):
        """
        __init__ sets up the header for the file.

        Params:
            - header    [list of independent variable tuples (name and num entries) and dependent variable tuples]
            - file      file name to write to
        """
        self.header = header
        self.file = file

    def add_source(self, source):
        """
        add_source adds a line to the data to write to the file.
        prereq that this is done IN ORDER.

        Params:
            - source    [list of characteristics]
        """
        self.data.append(source)

    def retrieve_source(self, params):
        """
        retrieve_source searches the file for matching independent conditions and retrieve the current 
        output if possible.
        
        Params:
            - params    [list of independent variables in column order to search]
        """
        if self.header == CELL_MODEL_HEADER:
            """
            temp has a range of [0, 80] and a resolution of 0.5
            irradiance has a range of [0, 1000] and a resolution of 50
            v_ref has a range of [0, 0.8] and a resolution of 0.01
            """

            # regularize input
            # NOTE: round because int() truncates, breaks things when val is like 0.9999998
            temp_idx = int(round(params[2]*2))      # 0.5 * 2 = 1
            irrad_idx = int(round(params[1]/50))    # 50. / 50 = 1
            v_ref_idx = int(round(params[0]*100))   # .01 * 100 = 1

            # same way you'd index a flattened 3d RGB array
            # 1 to ignore the header
            # 1000/50 + 1 = 21 number of irradiance entries per v_ref entry
            # 80/.5 + 1 = 161 number of temp entries per irradiance entry
            # 161 * 21 = 3381 number of temp entries per v_ref entry
            idx = 1 + temp_idx + 161 * irrad_idx + 3381 * v_ref_idx
            data = self.data[idx]

            # for each parameter in the list of independent variables
            for param_idx in range(len(params)):
                # check to see if we meet all of them, otherwise fail
                if round(float(data[param_idx]), 2) != round(params[param_idx], 2):
                    print("[RETRIEVE_SOURCE] [WARN] Matching params not found: ", params)
                    return 0
            return data[3]

        else:
            return 0

    def write_file(self):
        """
        write_file writes all of the accumulated data to the file.
        """
        if self.header == CELL_MODEL_HEADER:
            header = ["v_ref (V)", "irrad (G)", "temp (C)", "current (A)"]
        else:
            header = []

        with open(self.file, "w", newline='\n') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            for line in self.data:
                writer.writerow(line)

    def read_file(self):
        """
        Initializes data with contents of the file.
        """
        with open(self.file, "r", newline='\n') as csv_file:
            reader = csv.reader(csv_file)            
            for row in reader:
                self.data.append(row)
