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
# deprecating
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

# used for primary display and realtime update
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys


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


    cycles = []
    irradiances = []
    temps = []
    voltages = []
    currents = []
    powers = []

    iv_curve = [[], [], [], (0, 0, 0)]

    voltages2 = []
    currents2 = []
    powers2 = []

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
        
        self.app = QtGui.QApplication([])
        self.view = pg.GraphicsView()
        self.layout = pg.GraphicsLayout(border=(100, 100, 100))
        self.view.setCentralItem(self.layout)
        # Enable antialiasing for prettier plots and set to light theme
        pg.setConfigOptions( #TODO: set to white background with black text
            antialias=True,
            background=pg.mkColor(0, 0, 0),
            foreground=pg.mkColor(255, 255, 255)
        )

        # display window
        self.view.show()
        self.view.setWindowTitle('MPPT Simulator')
        self.view.resize(1200, 600)

    def add_datapoint(self, cycle, env_conditions, source, mppt):
        """
        addDatapoint
        adds a datapoint to each data structure corresponding to the inputs.
        
        Args:
            - cycle             (int): current simulation cycle.
            - env_conditions    (tuple): environmental conditions.
                (irrad, temp, load)
                - irrad   (float): irradiance
                - temp    (float): temperature (C)
                - load    (float): load on the system (W/s) NOTE: UNUSED

            - source:           [list] source IV curve and gmpp.
                (characteristics (list), (v_mpp, i_mpp, p_mpp))
                - characteristics is a list of [v_src, i_src].
                - all values are in float.
                - voltages: (V)
                - current: (A)
            - mppt:             (tuple): values for the mppt
                (v_mppt, i_mppt, p_mppt)
                - v_mppt  (float): mppt reference voltage (V)
                - i_mppt  (float): mppt induced current (A)
                - p_mppt  (float): mppt induced power (W)
        
        Returns:
            - None (NOTE: Possibly add error return here for handling exceptions?)
        """
        (characteristics, (v_mpp, i_mpp, p_mpp)) = source
        (v_mppt, i_mppt, p_mppt) = mppt
        # widget 1
        self.cycles.append(cycle)
        self.irradiances.append(env_conditions[0]/1000) # to get this in a visible range
        self.temps.append(env_conditions[1]/100) # to get this in a visible range
        self.voltages.append(source[1][0])
        self.currents.append(source[1][1])
        self.powers.append(source[1][2])

        # widget 2
        self.iv_curve = [[], [], [], (0, 0, 0)]
        for characteristic in characteristics:
            self.iv_curve[0].append(characteristic[0])
            self.iv_curve[1].append(characteristic[1])
            self.iv_curve[2].append(characteristic[0]*characteristic[1])
        self.iv_curve[3] = (mppt[0], mppt[1], mppt[0]*mppt[1])

        # widget 3
        self.voltages2.append(mppt[0])
        self.currents2.append(mppt[1])
        self.powers2.append(mppt[2])

        # widget 4
        # calculate secondary results
        p_mppt = v_mppt * i_mppt

        p_diff = 0
        if (p_mpp + p_mppt) != 0:
            p_diff = abs(p_mpp-p_mppt)/((p_mpp+p_mppt)/2)

        # find index to insert into for all lists
        insert_index = cycle

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

    def init_display(self, num_cells=1, cycle_start=0, cycle_end=0, time_step=1):
        """
        init_display TODO: manage num_cells to extend bounds
        sets up the display window. Call once (globally) before display.

        Args:
            - num_cells
            - cycle_start   (int): default 0 (the start of the simulation). left independent axis limit of the plot.
            - cycle_end     (int): default 0 (the start of the simulation). right independent axis limit of the plot.
            - time_step     (int): default 1 the interval of data to be shown. I.e. a time_step of 2 will hide every other data point.
                
        Return:
            - None
        """


        # widget 1 - source characteristics
        self.plt = self.layout.addPlot(
            title="Source Characteristics Over Time",
            row=0,
            col=0,
            rowspan=1,
            colspan=1
        )
        self.plt.addLegend()
        self.voltage1 = self.plt.plot(
            x=self.cycles, 
            y=self.voltages,
            pen=pg.mkPen((255, 0, 0), width=2),
            name="Voltage (V)"
        )
        self.current1 = self.plt.plot(
            x=self.cycles, 
            y=self.currents,
            pen=pg.mkPen((0, 255, 0), width=2),
            name="Current (A)"
        )
        self.power1 = self.plt.plot(
            x=self.cycles, 
            y=self.powers,
            pen=pg.mkPen((0, 0, 255), width=2),
            name="Power (W)"
        )
        self.irrad1 = self.plt.plot(
            x=self.cycles, 
            y=self.irradiances,
            pen=pg.mkPen((255, 0, 122), width=2),
            name="Irradiance (G/1000)"
        )
        self.temp1 = self.plt.plot(
            x=self.cycles, 
            y=self.temps,
            pen=pg.mkPen((255, 122, 0), width=2),
            name="Temperature (C/100)"
        )
        self.plt.setLabel('left', "Characteristics")
        self.plt.setLabel('bottom', "Cycle")


        # widget 2 - mppt v_ref overlayed on source IV curve
        self.plt2 = self.layout.addPlot(
            title="MPPT V_REF Over Source IV/PV Curve",
            row=0,
            col=1,
            rowspan=1,
            colspan=2
        )
        self.plt2.addLegend()
        self.iv_curve1 = self.plt2.plot(
            x=self.iv_curve[0],
            y=self.iv_curve[1],
            pen=pg.mkPen((255, 0, 0), width=2),
            name="Source IV Curve"
        )
        self.iv_curve2 = self.plt2.plot(
            x=self.iv_curve[0],
            y=self.iv_curve[2],
            pen=pg.mkPen((0, 255, 0), width=2),
            name="Source PV Curve"
        )
        self.scatter1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255))
        self.scatter1.addPoints([{'pos': [self.iv_curve[3][0], self.iv_curve[3][1]], 'data': 1}])
        self.plt2.addItem(self.scatter1)
        self.scatter2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255))
        self.scatter2.addPoints([{'pos': [self.iv_curve[3][0], self.iv_curve[3][2]], 'data': 1}])
        self.plt2.addItem(self.scatter2)
        self.plt2.setLabel('left', "Current (A)")
        self.plt2.setLabel('bottom', "Voltage (V)")


        # widget 3 - mppt characteristics
        self.plt3 = self.layout.addPlot(
            title="MPPT Characteristics Over Time",
            row=1,
            col=0,
            rowspan=1,
            colspan=1
        )
        self.plt3.addLegend()
        self.voltage2 = self.plt3.plot(
            x=self.cycles,
            y=self.voltages2,
            pen=pg.mkPen((255, 0, 0), width=2),
            name="Voltage (V)"
        )
        self.current2 = self.plt3.plot(
            x=self.cycles, 
            y=self.currents2,
            pen=pg.mkPen((0, 255, 0), width=2),
            name="Current (A)"
        )
        self.power2 = self.plt3.plot(
            x=self.cycles, 
            y=self.powers2,
            pen=pg.mkPen((0, 0, 255), width=2),
            name="Power (W)"
        )
        self.plt3.setLabel('left', "Characteristics")
        self.plt3.setLabel('bottom', "Cycle")


        # widget 4 - Power Comparison
        self.plt4 = self.layout.addPlot(
            title="Power Comparison Over Time",
            row=1,
            col=1,
            rowspan=1,
            colspan=1
        )
        self.plt4.addLegend()
        self.power3 = self.plt4.plot(
            x=self.cycles,
            y=self.powers,
            pen=pg.mkPen((255, 0, 0), width=2),
            name="Max Power (W)"
        )
        self.power4 = self.plt4.plot(
            x=self.cycles, 
            y=self.powers2,
            pen=pg.mkPen((0, 255, 0), width=2),
            name="MPPT Power (W)"
        )
        self.plt4.setLabel('left', "Power (W)")
        self.plt4.setLabel('bottom', "Cycle")

        # widget 5 - Tracking Efficiency
        self.plt5 = self.layout.addPlot(
            title="Efficiency Characteristics Over Time",
            row=1,
            col=2,
            rowspan=1,
            colspan=1
        )
        self.plt5.addLegend()
        self.eff1 = self.plt5.plot(
            x=self.cycles,
            y=self.disp_pDiff,
            pen=pg.mkPen((255, 0, 0), width=2),
            name="% Max Diff"
        )
        self.eff2 = self.plt5.plot(
            x=self.cycles, 
            y=self.disp_pDiffA,
            pen=pg.mkPen((0, 255, 0), width=2),
            name="% Cycles Above Threshold"
        )
        self.eff3 = self.plt5.plot(
            x=self.cycles, 
            y=self.disp_pEff,
            pen=pg.mkPen((0, 0, 255), width=2),
            name="% Tracking Efficiency"
        )
        self.plt5.setLabel('left', "Efficiency (%)")
        self.plt5.setLabel('bottom', "Cycle")

    def update_display(self, cycle_start=0, cycle_end=0, time_step=1):
        """
        update_display
        displays a pyqtgraph display based on the mode and current simulation values.
        
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
        # widget 1
        self.voltage1.setData(y=self.voltages[cycle_start:cycle_end:time_step])
        self.current1.setData(y=self.currents[cycle_start:cycle_end:time_step])
        self.power1.setData(y=self.powers[cycle_start:cycle_end:time_step])
        self.irrad1.setData(y=self.irradiances[cycle_start:cycle_end:time_step])
        self.temp1.setData(y=self.temps[cycle_start:cycle_end:time_step])

        # widget 2
        self.iv_curve1.setData(
            x=self.iv_curve[0],
            y=self.iv_curve[1]
        )
        self.iv_curve2.setData(
            x=self.iv_curve[0],
            y=self.iv_curve[2]
        )
        self.scatter1.setData([{'pos': [self.iv_curve[3][0], self.iv_curve[3][1]], 'data': 1}])
        self.scatter2.setData([{'pos': [self.iv_curve[3][0], self.iv_curve[3][2]], 'data': 1}])

        # widget 3
        self.voltage2.setData(
            x=self.cycles[cycle_start:cycle_end:time_step], 
            y=self.voltages2[cycle_start:cycle_end:time_step],
        )
        self.current2.setData(
            x=self.cycles[cycle_start:cycle_end:time_step], 
            y=self.currents2[cycle_start:cycle_end:time_step],
        )
        self.power2.setData(
            x=self.cycles[cycle_start:cycle_end:time_step], 
            y=self.powers2[cycle_start:cycle_end:time_step],
        )

        # widget 4
        self.power3.setData(y=self.powers)
        self.power4.setData(y=self.powers2)

        # widget 5
        self.eff1.setData(y=self.disp_pDiff)
        self.eff2.setData(y=self.disp_pDiffA)
        self.eff3.setData(y=self.disp_pEff)

        QtGui.QApplication.processEvents()

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

