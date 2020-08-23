"""
simulation.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/27/20
Last Modified: 8/22/20
Description: This Simulation class contains the state of the simulation. 
    It  1) collects data from the source and mppt
    and 2) displays it using matplotlib.
"""
# used for primary display and realtime update
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys
import csv

from bisect import bisect
import numpy as np
import math

VOLTAGE = 0
CURRENT = 1
POWER   = 2
TEMP    = 3
IRRAD   = 4
STD_IRRAD = 1.0
STD_TEMP = 0.25

class Simulation:
    cycles = []
    irrads = []
    temps = []
    voltages = []
    currents = []
    powers = []

    iv_curve = [[], [], [], (0, 0, 0)]

    voltages2 = []
    currents2 = []
    powers2 = []

    # stats
    disp_pDiff  = [] # % diff from max power for cycle x
    disp_pDiffA = [] # % of cycles > % diff from max power by cycle x
    disp_pEff   = [] # tracking efficiency

    mppt_name = ""
    fig = None
    fig_num = 0
    axs = None
    twin_ax = None

    sets_temps = []     # set for each cluster of temps for source model
    sets_irrads = []    # set for each cluster of irrad for source model

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
        self.irrads.append(env_conditions[0]/250) # to get this in a visible range
        self.temps.append(env_conditions[1]/25) # to get this in a visible range
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

        s_act_pwr = sum(self.powers2[1:insert_index])
        s_max_pwr = sum(self.powers[1:insert_index])
        tracking_eff = 0
        if s_max_pwr > 0:
            tracking_eff = s_act_pwr/s_max_pwr

        self.disp_pDiff.insert(insert_index, p_diff) # percentage difference
        self.disp_pDiffA.insert(insert_index, p_diffA) # % of cycles below threshold
        self.disp_pEff.insert(insert_index, tracking_eff) # tracking efficiency of the total power generated

    def add_datapoint_source_model(self, irrad, temp, v_src, i_src):
        """
        addDatapoint
        adds a datapoint to each data structure corresponding to the inputs.
        
        Args:
            - irrad   (float): irradiance
            - temp    (float): temperature (C)
            - v_src   (float): source voltage (V)
            - i_src   (float): source current (A)
        
        Returns:
            - None (NOTE: Possibly add error return here for handling exceptions?)
        """
        # calculate secondary results
        p_src = v_src * i_src
        temp = round(temp/100, 2)
        irrad = round(irrad/1000, 2)

        self.voltages.append(v_src)
        self.currents.append(i_src)
        self.powers.append(p_src)
        self.temps.append(temp)
        self.irrads.append(irrad)

        # grab the latest temp set
        # if we match add it, if we don't, make a new set
        cur_temp = -1.00
        if self.sets_temps != []:
            cur_temp = self.sets_temps[len(self.sets_temps)-1][TEMP][0]
        if irrad != STD_IRRAD:
            pass
        else:
            # if we're in a different temperature regime, make a new set
            if temp != cur_temp:
                cur_set_temp = [[], [], [], [], []]
                # Append data to the new set
                cur_set_temp[VOLTAGE].append(v_src)
                cur_set_temp[CURRENT].append(i_src)
                cur_set_temp[POWER].append(round(v_src*i_src, 2))
                cur_set_temp[TEMP].append(temp)
                cur_set_temp[IRRAD].append(irrad)
                self.sets_temps.append(cur_set_temp)
            else:
                cur_set_temp = self.sets_temps[len(self.sets_temps)-1]
                # Append data to the existing set
                cur_set_temp[VOLTAGE].append(v_src)
                cur_set_temp[CURRENT].append(i_src)
                cur_set_temp[POWER].append(round(v_src*i_src, 2))
                cur_set_temp[TEMP].append(temp)
                cur_set_temp[IRRAD].append(irrad)

        # grab the latest irrad set
        # if we match add it, if we don't, make a new set
        cur_irrad = -1.0
        if self.sets_irrads != []:
            cur_irrad = self.sets_irrads[len(self.sets_irrads)-1][IRRAD][0]
        if temp != STD_TEMP:
            pass
        else:
            # if we're in a different irradiance regime, make a new set
            if irrad != cur_irrad:
                cur_set_irrad = [[], [], [], [], []]
                # Append data to the new set
                cur_set_irrad[VOLTAGE].append(v_src)
                cur_set_irrad[CURRENT].append(i_src)
                cur_set_irrad[POWER].append(round(v_src*i_src, 2))
                cur_set_irrad[TEMP].append(temp)
                cur_set_irrad[IRRAD].append(irrad)
                self.sets_irrads.append(cur_set_irrad)
            else:
                cur_set_irrad = self.sets_irrads[len(self.sets_irrads)-1]
                # Append data to the existing set
                cur_set_irrad[VOLTAGE].append(v_src)
                cur_set_irrad[CURRENT].append(i_src)
                cur_set_irrad[POWER].append(round(v_src*i_src, 2))
                cur_set_irrad[TEMP].append(temp)
                cur_set_irrad[IRRAD].append(irrad)

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
        # display window
        self.view.show()
        self.view.setWindowTitle('MPPT Simulator')
        self.view.resize(1200, 600)

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
            y=self.irrads,
            pen=pg.mkPen((255, 0, 122), width=2),
            name="Irradiance (G/250)"
        )
        self.temp1 = self.plt.plot(
            x=self.cycles, 
            y=self.temps,
            pen=pg.mkPen((255, 122, 0), width=2),
            name="Temperature (C/25)"
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
            name="% Difference"
        )
        self.eff2 = self.plt5.plot(
            x=self.cycles, 
            y=self.disp_pDiffA,
            pen=pg.mkPen((0, 255, 0), width=2),
            name="% Cycles Above 5% Difference Threshold"
        )
        self.eff3 = self.plt5.plot(
            x=self.cycles, 
            y=self.disp_pEff,
            pen=pg.mkPen((0, 0, 255), width=2),
            name="% Tracking Efficiency"
        )
        self.plt5.setLabel('left', "Efficiency (%)")
        self.plt5.setLabel('bottom', "Cycle")

    def init_display_source_model(self):
        """
        init_display_source_model
        sets up the display window. Call once (globally) before display.

        Args:
            - None

        Return:
            - None
        """
        # display window
        self.view.show()
        self.view.setWindowTitle('Source Simulator')
        self.view.resize(1200, 600)

        # widget 1 - Effect of Temperature on IV and PV curve; IRRAD is set to 1000
        self.plt = self.layout.addPlot(
            title="IV Characteristic Dependence on Temperature @ 1000 G",
            row=0,
            col=0,
            rowspan=1,
            colspan=1
        )
        # plot the various series
        self.plots = []
        if self.sets_temps != []:
            for set_temp in self.sets_temps:
                self.plots.append([
                    self.plt.plot(
                        x=set_temp[VOLTAGE], 
                        y=set_temp[CURRENT],
                        pen=pg.mkPen((255, 255-set_temp[TEMP][0]*255, 255-set_temp[IRRAD][0]*255), width=2),
                    ),
                    self.plt.plot(
                        x=set_temp[VOLTAGE], 
                        y=set_temp[POWER],
                        pen=pg.mkPen((255, 255-set_temp[TEMP][0]*255, 255-set_temp[IRRAD][0]*255), width=2),
                    )
                ])
        self.plots_len = len(self.plots)
        self.plt.setLabel('left', "Current (A)")
        self.plt.setLabel('bottom', "Voltage (V)")
        
        # widget 2 - Effect of Irradiance on IV and PV curve; TEMP is set to 25
        self.plt2 = self.layout.addPlot(
            title="IV Characteristic Dependence on Irradiance @ 25 C",
            row=0,
            col=1,
            rowspan=1,
            colspan=1
        )
        # plot the various series
        self.plots2 = []
        if self.sets_irrads != []:
            for set_irrad in self.sets_irrads:
                self.plots2.append([
                    self.plt2.plot(
                        x=set_irrad[VOLTAGE], 
                        y=set_irrad[CURRENT],
                        pen=pg.mkPen((255, 255-set_irrad[TEMP][0]*255, set_irrad[IRRAD][0]*255), width=2),
                    ),
                    self.plt2.plot(
                        x=set_irrad[VOLTAGE], 
                        y=set_irrad[POWER],
                        pen=pg.mkPen((255, 255-set_irrad[TEMP][0]*255, set_irrad[IRRAD][0]*255), width=2),
                    )
                ])
        self.plots2_len = len(self.plots2)
        self.plt2.setLabel('left', "Current (A)")
        self.plt2.setLabel('bottom', "Voltage (V)")

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
        self.irrad1.setData(y=self.irrads[cycle_start:cycle_end:time_step])
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

    def update_display_source_model(self):
        """
        update_display_source_model
        sets up the display window for the source model.

        Args:
            - None
        
        Return:
            - None
        """
        # we should just check the most recent set
        # if it's not plotted, plot it, otherwise edit the existing one.

        # widget 1 - Effect of Temperature on IV and PV curve; IRRAD is set to 1000
        # plot the various series
        if len(self.sets_temps) > 0 and self.plots_len >= 0:
            # data sets | plots
            # 0 | 0, do nothing
            # 1 | 0, add a plot
            # 1 | 1, update plot [0, 1)
            # 2 | 1, update plot [0, 1), add a plot
            # 2 | 2, update plot [1, 2)
            # 4 | 2, update plot [1, 2), add two plots
            idx = self.plots_len -1
            if idx < 0:
                idx = 0
            for set_temp in self.sets_temps[idx:]:
                # modify existing
                if idx < len(self.plots):
                    self.plots[idx][0].setData(
                        x=set_temp[VOLTAGE], 
                        y=set_temp[CURRENT],
                        pen=pg.mkPen((255, 255-set_temp[TEMP][0]*255, 255-set_temp[IRRAD][0]*255), width=2),
                    )
                    self.plots[idx][1].setData(
                        x=set_temp[VOLTAGE], 
                        y=set_temp[POWER],
                        pen=pg.mkPen((255, 255-set_temp[TEMP][0]*255, 255-set_temp[IRRAD][0]*255), width=2),
                    )
                # add new
                else:
                    self.plots.append([
                        self.plt.plot(
                            x=set_temp[VOLTAGE], 
                            y=set_temp[CURRENT],
                            pen=pg.mkPen((255, 255-set_temp[TEMP][0]*255, 255-set_temp[IRRAD][0]*255), width=2),
                        ),
                        self.plt.plot(
                            x=set_temp[VOLTAGE], 
                            y=set_temp[POWER],
                            pen=pg.mkPen((255, 255-set_temp[TEMP][0]*255, 255-set_temp[IRRAD][0]*255), width=2),
                        )
                    ])
                idx += 1
        self.plots_len = len(self.plots)

        # widget 2 - Effect of Irradiance on IV and PV curve; TEMP is set to 25
        # plot the various series
        if len(self.sets_irrads) > 0 and self.plots2_len >= 0:
            idx = self.plots2_len - 1
            if idx < 0:
                idx = 0
            for set_irrad in self.sets_irrads[idx:]:
                # modify existing
                if idx < len(self.plots2):
                    self.plots2[idx][0].setData(
                        x=set_irrad[VOLTAGE], 
                        y=set_irrad[CURRENT],
                        pen=pg.mkPen((255, 255-set_irrad[TEMP][0]*255, set_irrad[IRRAD][0]*255), width=2),
                    )
                    self.plots2[idx][1].setData(
                        x=set_irrad[VOLTAGE], 
                        y=set_irrad[POWER],
                        pen=pg.mkPen((255, 255-set_irrad[TEMP][0]*255, set_irrad[IRRAD][0]*255), width=2),
                    )
                # add new
                else:
                    self.plots2.append([
                        self.plt2.plot(
                            x=set_irrad[VOLTAGE], 
                            y=set_irrad[CURRENT],
                            pen=pg.mkPen((255, 255-set_irrad[TEMP][0]*255, set_irrad[IRRAD][0]*255), width=2),
                        ),
                        self.plt2.plot(
                            x=set_irrad[VOLTAGE], 
                            y=set_irrad[POWER],
                            pen=pg.mkPen((255, 255-set_irrad[TEMP][0]*255, set_irrad[IRRAD][0]*255), width=2),
                        )
                    ])
                idx += 1
        self.plots2_len = len(self.plots2)

        QtGui.QApplication.processEvents()

    def overlay_data(self, file=""):
        if file != "":
            array = []
            with open(file, "r", newline='\n') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    array.append(row)
            array_formatted = []
            for item in array:
                item2 = {'pos': [float(item[0]), float(item[1])], 'brush': pg.mkBrush(int(item[2]), int(item[3]), int(item[4]))}
                array_formatted.append(item2)
            scatterPoints = pg.ScatterPlotItem(size=2, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255))
            scatterPoints.addPoints(array_formatted)
            self.plt2.addItem(scatterPoints)

    def save_model(self):
        with open("results.csv", "ab") as f:
            a = np.transpose(np.asarray([self.disp_cycle, self.disp_pDiff]))
            np.savetxt(f, a, delimiter=",", fmt='%.4f')