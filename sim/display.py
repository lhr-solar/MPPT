"""
Display.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This file describes the Display class, which does 3 things:
    - Graphs the Vref/Iin/Pout and Vin/Iin/Pmax of the system
    - Performs data diagnostics, including:
        - For a static source: graphs the % diff between Pout and Pmax over time/iteration 
        - For a dynamic source: graphs the % cycles > x% diff from max power as well as the previous point.
"""

class Display:
    def __init__(self):
        """
        init
        """
        return

    def read_data(Vref, Iin, Pout, Pmax):
        """
        read_data 
        Takes in system inputs and updates its data structure. Performs any calculations needed.

        """
        return

    def calculate_efficiency():
        """
        calculate_efficiency
        Determines two statistics: 
            - the % of the current supplied power to the max theoretical power
            - the % of cycles where the supplied power > x% diff from the max theoretical power
            - the avg number of cycles to get within a y% diff from the max theoretical power. Discounts events where the input conditions change faster than the avg number.
        """
        return

    def display_results():
        """
        display_results
        Runs the kivy widgets to display the data.
        """
        return
