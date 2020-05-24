"""
main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 5/24/20
Description: This is the main handler for the mppt simulator. 
  It uses Kivy for the UI of this application, in particular the graphs and statistics.
  The simulator has three main components:
      1. Source simulator - The program simulates a solar cell or set of solar cells by taking in static parameters or a datafile of input values over time.
      2. MPPT Algorithm - A black box that manages algorithms (PandO, Incr. Conduction, RCC, Fuzzy Logic, etc) to maximize power on the load.
      3. Display - The outputs of the MPPT and the source are calculated and graphed. Data over time will be evaluated to determine and compare efficiencies between algorithms.
"""

import Source
import PandO
import Display

if __name__=="__main__":
    main()
else:
    print("Run main.py as a script.")


def main():
    source = Source()
    mppt = PandO()
    display = Display()

    # for each iteration (or until user cancel, based on the mode), run each of the 3 components in order.
