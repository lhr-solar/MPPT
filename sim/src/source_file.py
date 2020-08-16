"""
source_file.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 8/15/20
Last Modified: 8/15/20

Description: This file is a standalone file that can be inserted into a program to read and write
    an encoded model from a .csv. This speeds up model calculations.

    Generates a high fidelity model of the source and encodes it into a csv file.
    This can be used by other programs to quickly grab and interpolate data given a keyed set of 
    independent conditions.
    
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
    We can retrieve the data using consecutive binary search across columns. That is, we find the 
    section of entries corresponding to the correct v_ref, then irradiance, then temp, and so on.

    Other optimizations could potentially be included, involving the storage of the independent 
    variable bounds to compress the search space. (That is, we can run a first pass read and hold
    the range that all V is 0 -say, (0, 45) and can skip looking at all those lines with fseek if
    we're not looking for V=0.)

    If we can't find the entry, we need to interpolate between the closest 2^n points. For example,
    say we only have v_ref and irradiance as independent variables. Say we have the four corners as 
    entries, but we want to find (5, 5). We need to perform bilinear interpolation to get (5, 5).

    (0, 0) ...... (10, 0)
       .             .
       .             .
       .   (5, 5)    .
       .             .
       .             .
    (0, 10)..... (10, 10)

    With three dimensions (v_ref, irradiance, temp), we need to perform trilinear interpolation.

    These problems have two parts:
        1) Finding the corners
        2) Performing interpolation.

    An alternative solution is running a single pass file read to build a dictionary upon 
    initialization, which is very fast, but does not support interpolation without a more complex 
    data scheme (i.e. linked list to corners that need to be updated during the first pass search 
    continuously).
"""
import csv


class SourceFile():
    header = []
    data = []
    file = ""
    
    def __init__(self, header=["v_ref (V)", "irrad (G)", "temp (C)", "current (A)"], file="model.csv"):
        """
        __init__ sets up the header for the file.

        Params:
            - header    [list of column names]
            - file     file name to write to
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
        searches file for independent conditions and retrieve the current output if possible.
        
        Params:
            - params    [list of independent variables in column order to search]
        """
        pass

    def write_file(self):
        """
        write_file writes all of the accumulated data to the file
        """
        with open(self.file, "w", newline='\n') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.header)
            for line in self.data:
                writer.writerow(line)

    def read_file(self):
        """
        Initializes data with contents of the file, perhaps with some optimizing information.
        """
        pass
