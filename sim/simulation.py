"""
simulation.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/27/20
Last Modified: 5/28/20
Description: This Simulation class contains the state of the simulation. 
    It  1) collects data from the source and mppt
    and 2) displays it using matplotlib.
"""
import matplotlib
import matplotlib.pyplot as plt
from bisect import bisect
import numpy as np
import math

class Simulation:
    disp_cycle  = []
    # source output
    disp_vsrc   = []
    disp_isrc   = []
    disp_psrc   = []
    # mppt output
    disp_vref   = []
    disp_pref   = []
    # tunable parameters
    disp_temp   = []
    disp_irrad  = []
    disp_load   = []
    # stats
    disp_pDiff  = [] # % diff from max power for cycle x
    disp_pDiffA = [] # % of cycles > % diff from max power by cycle x

    disp_open = False

    fig = None
    fig_num = 0
    axs = None
    twin_ax = None

    def __init__(self, mppt_name):
        """
        init

        Args:
            - mppt_name (String): name of MPPT Algorithm to be displayed
        """
        plt.ion()
        self.fig, self.axs = plt.subplots(2, 2)
        self.fig.set_size_inches(9, 10)

        self.axs[0, 0].set_xlabel('Cycle')
        self.axs[0, 0].set_ylabel('Volt. (V), Curr (A), and Pwr. (W)')
        self.axs[0, 0].set_ylim([0, 7])
        self.twin_ax = self.axs[0, 0].twinx()
        self.twin_ax.set_ylabel('Temperature (C)')
        self.twin_ax.set_ylim([0, 200])
        self.axs[0, 0].set_title('Source Characteristics Over Time')

        self.axs[1, 0].set_xlabel('Cycle')
        self.axs[1, 0].set_ylabel('Volt. (V), Curr (A), and Pwr. (W)')
        self.axs[1, 0].set_ylim([0, 7])
        self.axs[1, 0].set_title('MPPT Characteristics Over Time')

        self.axs[0, 1].set_xlabel('Cycle')
        self.axs[0, 1].set_ylabel('Max Pwr (W) and Actual Pwr (W)')
        self.axs[0, 1].set_ylim([0, 4])
        self.axs[0, 1].set_title('Power Comparison Over Time')

        self.axs[1, 1].set_xlabel('Cycle')
        self.axs[1, 1].set_ylabel('% Diff from Max Pwr and % Ratio Diff')
        self.axs[1, 1].set_ylim([0, 1])
        self.axs[1, 1].set_title('Power Comparison Over Time')

        self.fig.suptitle(mppt_name)
        plt.tight_layout()

        self.fig_num = plt.gcf().number
        print("Fig num:", self.fig_num)
        return

    def addDatapoint(self, cycle, irrad, temp, load, v_src, i_src, v_ref):
        """
        addDatapoint
        adds a datapoint to each data structure corresponding to the inputs.
        
        Args:
            - cycle     (int): current simulation cycle.
            - irrad   (float): irradiance
            - temp    (float): temperature (C)
            - load    (float): load on the system (W/s) NOTE: UNUSED
            - v_src   (float): source voltage (V)
            - i_src   (float): source current (A)
            - v_ref   (float): mppt reference voltage (V)
        
        Returns:
            - None (NOTE: Possibly add error return here for handling exceptions?)
        """
        # calculate secondary results
        p_src = v_src * i_src
        p_ref = v_ref * i_src

        p_diff = 0
        if (p_src + p_ref) != 0:
            p_diff = abs(p_src-p_ref)/((p_src+p_ref)/2)

        # find index to insert into for all lists
        insert_index = bisect(self.disp_cycle, cycle)

        # grab prev entry's p_diffA
        prev_p_diffA = 0
        if insert_index > 0:
            prev_p_diffA = self.disp_pDiffA[insert_index - 1]

        #TODO: redefine threshold somewhere else, maybe in init/setup
        threshold = .05
        if p_diff > threshold:
            p_diffA = (prev_p_diffA*(insert_index) + 1)/(insert_index + 1) # 1 index insert_index
        else:
            p_diffA = (prev_p_diffA*(insert_index))/(insert_index + 1) # 1 index insert_index

        self.disp_cycle.insert(insert_index, cycle)
        self.disp_vsrc.insert(insert_index, v_src)
        self.disp_isrc.insert(insert_index, i_src)
        self.disp_psrc.insert(insert_index, p_src)
        self.disp_vref.insert(insert_index, v_ref)
        self.disp_pref.insert(insert_index, p_ref)
        
        self.disp_temp.insert(insert_index, temp)
        self.disp_irrad.insert(insert_index, irrad)
        self.disp_load.insert(insert_index, load)
        
        self.disp_pDiff.insert(insert_index, p_diff)
        self.disp_pDiffA.insert(insert_index, p_diffA)
        return

    def getDatapoint(self, cycle):
        """
        printDatapoint
        Gets a datapoint given a cycle in time.

        Args:
            - cycle     (int): simulation cycle that points should be retrieved from
        
        Returns:
            - [cycle, v_src, i_src, p_src, v_ref, p_ref, temp, irrad, load, pDiff, pDiffA]
        """
        try:
            idx = self.disp_cycle.index(cycle)
            data = [self.disp_cycle[idx], 
                self.disp_vsrc[idx], self.disp_isrc[idx], self.disp_psrc[idx],
                self.disp_vref[idx], self.disp_pref[idx],
                self.disp_temp[idx], self.disp_irrad[idx], self.disp_load[idx],
                self.disp_pDiff[idx], self.disp_pDiffA[idx]
            ]
            return data
        except ValueError:
            print("[SIMULATION] Error: Cycle does not exist in data.")

    def display(self, cycle_start=0, cycle_end=0, time_step=1):
        """
        display TODO: implement time_step
        displays a matplotlib display based on the mode and current simulation values.
        
        Modes:
            - source    - voltage/current/power of the source
            - mppt      - current of the source and voltage/power of the mppt
            - power     - compares source and mppt power
            - stats     - displays % diff over time between source/mppt power and % of cycles below a certain % diff
        
        Args:
            - cycle_start   (int): default 0 (the start of the simulation). left independent axis limit of the plot.
            - cycle_end     (int): default 0 (the start of the simulation). right independent axis limit of the plot.
            - time_step     (int): default 1 the interval of data to be shown. I.e. a time_step of 2 will hide every other data point.
        
        Returns:
            - None
        """
        t_cycle     = self.disp_cycle[cycle_start:cycle_end]
        t_disp_vsrc = self.disp_vsrc[cycle_start:cycle_end]
        t_disp_isrc = self.disp_isrc[cycle_start:cycle_end]
        t_disp_psrc = self.disp_psrc[cycle_start:cycle_end]
        t_disp_vref = self.disp_vref[cycle_start:cycle_end]
        t_disp_pref = self.disp_pref[cycle_start:cycle_end]

        t_disp_pDiff    = self.disp_pDiff[cycle_start:cycle_end]
        t_disp_pDiffA   = self.disp_pDiffA[cycle_start:cycle_end]

        t_disp_temp     = self.disp_temp[cycle_start:cycle_end]
        # check if figure still exists
        if not plt.fignum_exists(self.fig_num):
            self.__init__()

        # source
        self.axs[0, 0].plot(t_cycle, t_disp_vsrc, color='r', marker='o', markersize=2)
        self.axs[0, 0].plot(t_cycle, t_disp_isrc, color='g', marker='v', markersize=2)
        self.axs[0, 0].plot(t_cycle, t_disp_psrc, color='b', marker='D', markersize=2)
        self.axs[0, 0].legend(labels=('Voltage', 'Current', 'Power'), loc="upper left")
        self.twin_ax.plot(t_cycle, t_disp_temp, color='k', marker='1', markersize=2)
        self.twin_ax.legend(labels=('Temp'), loc="upper right")

        # mppt
        self.axs[1, 0].plot(t_cycle, t_disp_vref, color='r', marker='o', markersize=2)
        self.axs[1, 0].plot(t_cycle, t_disp_isrc, color='g', marker='v', markersize=2)
        self.axs[1, 0].plot(t_cycle, t_disp_pref, color='b', marker='D', markersize=2)
        self.axs[1, 0].legend(labels=('Voltage', 'Current', 'Power'), loc="upper left")

        # power
        self.axs[0, 1].plot(t_cycle, t_disp_psrc, color='r', marker='o', markersize=2)
        self.axs[0, 1].plot(t_cycle, t_disp_pref, color='b', marker='D', markersize=2)
        self.axs[0, 1].legend(labels=('Max', 'Actual'), loc="upper left")

        # cycle stats
        self.axs[1, 1].plot(t_cycle, t_disp_pDiff, color='r', marker='o', markersize=2)
        self.axs[1, 1].plot(t_cycle, t_disp_pDiffA, color='b', marker='D', markersize=2)
        self.axs[1, 1].legend(labels=('% Max Diff', '% Cycles Above Threshold'), loc="upper left")

        plt.tight_layout()
        plt.draw()

