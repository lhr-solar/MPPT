"""
simulation.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/27/20
Last Modified: 8/15/20
Description: This Simulation class contains the state of the simulation. 
    It  1) collects data from the source and mppt
    and 2) displays it using matplotlib.
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from bisect import bisect
import numpy as np
import math

class Simulation:
    disp_cycle  = []
    # source output
    disp_vsrc   = []
    disp_isrc   = []
    disp_psrc   = []
    disp_vmpp   = []
    disp_impp   = []

    # mppt output
    disp_vmppt  = []
    disp_imppt  = []
    disp_pmppt  = []
    # tunable parameters
    disp_temp   = []
    disp_irrad  = []
    disp_load   = []
    # stats
    disp_pDiff  = [] # % diff from max power for cycle x
    disp_pDiffA = [] # % of cycles > % diff from max power by cycle x
    disp_pEff   = [] # tracking efficiency

    disp_open = False

    mppt_name = ""
    fig = None
    fig_num = 0
    axs = None
    twin_ax = None

    def __init__(self, mppt_name=""):
        """
        init

        Args:
            - mppt_name (String): name of MPPT Algorithm to be displayed
        """
        self.mppt_name = mppt_name

    def add_datapoint(self, cycle, irrad, temp, load, v_src, i_src, v_mppt, i_mppt):
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
            - v_mppt  (float): mppt reference voltage (V)
            - i_mppt  (float): mppt induced current (V)
        
        Returns:
            - None (NOTE: Possibly add error return here for handling exceptions?)
        """
        # calculate secondary results
        p_src = v_src * i_src
        p_mppt = v_mppt * i_mppt

        p_diff = 0
        if (p_src + p_mppt) != 0:
            p_diff = abs(p_src-p_mppt)/((p_src+p_mppt)/2)

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

        s_act_pwr = sum(self.disp_pmppt[1:insert_index])
        s_max_pwr = sum(self.disp_psrc[1:insert_index])
        tracking_eff = 0
        if s_max_pwr > 0:
            tracking_eff = s_act_pwr/s_max_pwr

        self.disp_cycle.insert(insert_index, cycle)

        self.disp_vsrc.insert(insert_index, v_src)
        self.disp_isrc.insert(insert_index, i_src)
        self.disp_psrc.insert(insert_index, p_src)

        self.disp_vmppt.insert(insert_index, v_mppt)
        self.disp_imppt.insert(insert_index, i_mppt)
        self.disp_pmppt.insert(insert_index, p_mppt)
        
        self.disp_temp.insert(insert_index, temp)
        self.disp_irrad.insert(insert_index, irrad/10)
        self.disp_load.insert(insert_index, load)
        
        self.disp_pDiff.insert(insert_index, p_diff)
        self.disp_pDiffA.insert(insert_index, p_diffA)
        self.disp_pEff.insert(insert_index, tracking_eff)

    def add_datapoint_source_model(self, irrad, temp, load, v_src, i_src):
        """
        addDatapoint
        adds a datapoint to each data structure corresponding to the inputs.
        
        Args:
            - irrad   (float): irradiance
            - temp    (float): temperature (C)
            - load    (float): load on the system (W/s) NOTE: UNUSED
            - v_src   (float): source voltage (V)
            - i_src   (float): source current (A)
        
        Returns:
            - None (NOTE: Possibly add error return here for handling exceptions?)
        """
        # calculate secondary results
        p_src = v_src * i_src

        self.disp_vsrc.append(v_src)
        self.disp_isrc.append(i_src)
        self.disp_psrc.append(p_src)

        self.disp_temp.append(temp)
        self.disp_irrad.append(irrad)
        self.disp_load.append(load)

    def get_datapoint(self, cycle):
        """
        printDatapoint
        Gets a datapoint given a cycle in time.

        Args:
            - cycle     (int): simulation cycle that points should be retrieved from
        
        Returns: 
            - [cycle, v_src, i_src, p_src, v_mppt, i_mppt, p_mppt, temp,
                irrad, load, pDiff, pDiffA]
        """
        try:
            idx = self.disp_cycle.index(cycle)
            data = [self.disp_cycle[idx], 
                self.disp_vsrc[idx],    self.disp_isrc[idx],    self.disp_psrc[idx],
                self.disp_vmppt[idx],   self.disp_imppt[idx],   self.disp_pmppt[idx],
                self.disp_temp[idx],    self.disp_irrad[idx],   self.disp_load[idx],
                self.disp_pDiff[idx],   self.disp_pDiffA[idx]
            ]
            return data
        except ValueError:
            print("[SIMULATION] Error: Cycle does not exist in data.")

    def init_display(self, num_cells=1):
        """
        init_display
        sets up the display window. Call once (globally) before display.

        Args:
            - None
        
        Return:
            - None
        """
        # our predictions of max voltage and current
        MAX_VOLTAGE = .8
        MAX_CURRENT = 6
        SCALING = .8
        source_lim = 7
        if num_cells > 2:
            source_lim += ((num_cells-1) * MAX_VOLTAGE * MAX_CURRENT) * SCALING
        power_lim = 7 
        if num_cells > 2:
            power_lim += num_cells * MAX_VOLTAGE * MAX_CURRENT * SCALING

        self.fig, self.axs = plt.subplots(2, 2)
        self.fig.set_size_inches(9, 10)

        self.axs[0, 0].set_xlabel('Cycle')
        self.axs[0, 0].set_ylabel('Volt. (V), Curr (A), and Pwr. (W)')
        self.axs[0, 0].set_ylim([0, source_lim])
        self.twin_ax = self.axs[0, 0].twinx()
        self.twin_ax.set_ylabel('Irradiance (10s of W/m^2), Temp (C)')
        self.twin_ax.set_ylim([0, 150])
        self.axs[0, 0].set_title('Source Characteristics Over Time')

        self.axs[1, 0].set_xlabel('Cycle')
        self.axs[1, 0].set_ylabel('Volt. (V), Curr (A), and Pwr. (W)')
        self.axs[1, 0].set_ylim([0, power_lim])
        self.axs[1, 0].set_title('MPPT Characteristics Over Time')

        self.axs[0, 1].set_xlabel('Cycle')
        self.axs[0, 1].set_ylabel('Max Pwr (W) and Actual Pwr (W)')
        self.axs[0, 1].set_ylim([0, power_lim])
        self.axs[0, 1].set_title('Power Comparison Over Time')

        self.axs[1, 1].set_xlabel('Cycle')
        self.axs[1, 1].set_ylabel('% Diff from Max Pwr, % Ratio Diff, Tracking Eff.')
        self.axs[1, 1].set_ylim([0, 1])
        self.axs[1, 1].set_title('Power Comparison Over Time')

        self.fig.suptitle(self.mppt_name)
        plt.tight_layout()

        self.fig_num = plt.gcf().number
        print("[SIMULATION] Fig num:", self.fig_num)

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

        t_disp_vmppt = self.disp_vmppt[cycle_start:cycle_end]
        t_disp_imppt = self.disp_imppt[cycle_start:cycle_end]
        t_disp_pmppt = self.disp_pmppt[cycle_start:cycle_end]

        t_disp_pDiff    = self.disp_pDiff[cycle_start:cycle_end]
        t_disp_pDiffA   = self.disp_pDiffA[cycle_start:cycle_end]
        t_disp_teff     = self.disp_pEff[cycle_start:cycle_end]

        t_disp_temp     = self.disp_temp[cycle_start:cycle_end]
        t_disp_irrad    = self.disp_irrad[cycle_start:cycle_end]
        # check if figure still exists
        if not plt.fignum_exists(self.fig_num):
            self.__init__()

        # source
        self.axs[0, 0].plot(t_cycle, t_disp_vsrc, color='r', marker='o', markersize=1)
        self.axs[0, 0].plot(t_cycle, t_disp_isrc, color='g', marker='v', markersize=1)
        self.axs[0, 0].plot(t_cycle, t_disp_psrc, color='b', marker='D', markersize=1)
        self.axs[0, 0].legend(labels=('Voltage', 'Current', 'Power'), loc="upper left")
        self.twin_ax.plot(t_cycle, t_disp_irrad, color='y', marker='>', markersize=1)
        self.twin_ax.plot(t_cycle, t_disp_temp, color='k', marker='1', markersize=1)
        self.twin_ax.legend(labels=('Irradiance', 'Temp'), loc="upper right")

        # mppt
        self.axs[1, 0].plot(t_cycle, t_disp_vmppt, color='r', marker='o', markersize=1)
        self.axs[1, 0].plot(t_cycle, t_disp_imppt, color='g', marker='v', markersize=1)
        self.axs[1, 0].plot(t_cycle, t_disp_pmppt, color='b', marker='D', markersize=1)
        self.axs[1, 0].legend(labels=('Voltage', 'Current', 'Power'), loc="upper left")

        # power
        self.axs[0, 1].plot(t_cycle, t_disp_psrc, color='r', marker='o', markersize=1)
        self.axs[0, 1].plot(t_cycle, t_disp_pmppt, color='b', marker='D', markersize=1)
        self.axs[0, 1].legend(labels=('Max', 'Actual'), loc="upper left")

        # cycle stats
        self.axs[1, 1].plot(t_cycle, t_disp_pDiff, color='r', marker='o', markersize=1)
        self.axs[1, 1].plot(t_cycle, t_disp_pDiffA, color='b', marker='D', markersize=1)
        self.axs[1, 1].plot(t_cycle, t_disp_teff, color='g', marker='v', markersize=1)
        self.axs[1, 1].legend(labels=('% Max Diff', '% Cycles Above Threshold', '% Eff'), loc="upper left")

        plt.tight_layout()
        plt.show()

    def display_source_model(self, mode="Temperature"):
        """
        display_source_model
        sets up the display window for the source model.

        Args:
            - mode (String): What sort of model dependency should be displayed.
                Irradiance | Temperature | Both
        
        Return:
            - None
        """

        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax  = fig.add_subplot(1,2,1, projection='3d')
        ax2 = fig.add_subplot(1,2,2, projection='3d')

        if mode == "Irradiance":
            idx = 0
            for obj in self.disp_vsrc:
                X = self.disp_vsrc[idx]
                Y = self.disp_irrad[idx]
                Z = self.disp_isrc[idx]
                Z2= self.disp_psrc[idx]
                idx += 1
                ax.scatter(X, Y, Z, marker='o', color=[X/1, Y/1000, Z/10.0])
                ax2.scatter(X, Y, Z2, marker='o', color=[X/1, Y/1000, Z/10.0])
            
            ax.set_xlabel('Voltage (V)')
            ax.set_ylabel('Irradiance (W/m^2)')
            ax.set_zlabel('Current (I)')
            ax2.set_xlabel('Voltage (V)')
            ax2.set_ylabel('Irradiance (W/m^2)')
            ax2.set_zlabel('Power (W)')

        elif mode == "Temperature": # default temp
            idx = 0
            for obj in self.disp_vsrc:
                X = self.disp_vsrc[idx]
                Y = self.disp_temp[idx]
                Z = self.disp_isrc[idx]
                Z2= self.disp_psrc[idx]
                idx += 1
                ax.scatter(X, Y, Z, marker='o', color=[X/1, Y/120, Z/10.0])
                ax2.scatter(X, Y, Z2, marker='o', color=[X/1, Y/120, Z/10.0])
            
            ax.set_xlabel('Voltage (V)')
            ax.set_ylabel('Temperature (C)')
            ax.set_zlabel('Current (I)')
            ax2.set_xlabel('Voltage (V)')
            ax2.set_ylabel('Temperature (C)')
            ax2.set_zlabel('Power (W)')
        
        else:
            idx = 0
            for obj in self.disp_vsrc:
                X = self.disp_vsrc[idx]
                Y = self.disp_temp[idx]
                Z = self.disp_irrad[idx]
                ax.scatter(X, Y, Z, marker='o', color=[
                    X/1, 
                    Y/120,
                    Z/1200
                ], alpha=self.disp_isrc[idx]/10.0)
                ax2.scatter(X, Y, Z, marker='o', color=[
                    X/1, 
                    Y/120,
                    Z/1200
                ], alpha=self.disp_psrc[idx]/10.0)
                idx += 1

            ax.set_xlabel('Voltage (V)')
            ax.set_ylabel('Temperature (C)')
            ax.set_zlabel('Irradiance (G)')

            ax2.set_xlabel('Voltage (V)')
            ax2.set_ylabel('Temperature (C)')
            ax2.set_zlabel('Irradiance (G)')

        fig.suptitle(self.mppt_name) # but this is actually source model name
        plt.show()

    def save_model(self):
        with open("results.csv", "ab") as f:
            a = np.transpose(np.asarray([self.disp_cycle, self.disp_pDiff]))
            np.savetxt(f, a, delimiter=",", fmt='%.4f')

