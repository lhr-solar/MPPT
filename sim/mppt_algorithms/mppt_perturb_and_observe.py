"""
mppt_perturb_and_observe.py

P&O Algorithm function declarations
Fall 2017 MPPT using the Nucleo-L432KC (Pholociraptor)

Author: Samantha Guu
Team: Samuel Chiu, Madeline Drake, Kyle Grier, Rafael Ibanez, Chase Lansdale,
      Brooks Loper
Created on: November 12, 2017
Revised on: November 14, 2017
--------------------------------------------------------------------------------

Adapted by Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Last Modified: 5/28/20
"""
from .mppt import MPPT
class PandO(MPPT):
    # overload iterate method
    def iterate(self, v_in, i_in, t_in, cycle):
        """
        iterate TODO: Add paper
        Runs a single iteration of the PandO algorithm.

        Args:
            - v_in (float): source voltage (V)
            - i_in (float): source current (A)
            - t_in (float): temperature
            - cycle (int): current simulation cycle
            
        Returns:
            - v_ref (float): output voltage (V)

        Ref: 
            1. Developing Solar Inverter Control with Simulink
                - Part 3: Designing the MPPT Algorithm and Generating Production Code for the TI C2000 Microcontroller (Jonathan LeSage)
                - https://www.mathworks.com/videos/developing-solar-inverter-control-with-simulink-part-3-designing-the-mppt-algorithm-and-generating-production-code-for-the-ti-c2000-microcontroller-1554990116706.html
        """
        if (cycle % self.sample_rate) is 0: #sampling this run
            # compute power
            p_in = v_in * i_in
            # determine deltas
            diff_V = v_in - self.v_old
            diff_P = p_in - self.p_old

            print("[PANDO] Change Voltage: ", diff_V)
            print("[PANDO] Change Power: ", diff_P)

            dV_ref = self.calc_perturb_amt(self.v_ref, v_in, i_in, t_in)
            if diff_P > 0:
                if diff_V > 0:  # increase v_ref
                    self.v_ref += dV_ref
                else:       # decrease v_ref
                    self.v_ref -= dV_ref
            else:
                if diff_V > 0:  # decrease v_ref
                    self.v_ref -= dV_ref
                else:       # increase v_Ref
                    self.v_ref += dV_ref

            # update values
            self.v_old = v_in
            self.i_old = i_in
            self.p_old = p_in
            
        return self.v_ref

    def get_name(self):
        """
        get_name
        Returns mppt algorithm name.
        
        Args:
            - None

        Returns:
            - Name (String)
        """
        return "Perturb and Observe"