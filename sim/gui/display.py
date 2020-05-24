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
import os
import random

import kivy   
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import kivy.properties as kp

from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib import use as mpl_use

mpl_use('module://kivy.garden.matplotlib.backend_kivy')
style.use('dark_background')

build_string = Builder.load_file("./gui/display.kv")


class ProfileScreen(Screen):
    pass

class SandboxScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class ScreenManager(ScreenManager):
    pass


class Chart(BoxLayout):
    data = kp.ListProperty([])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fig, self.ax1 = plt.subplots()
        self.ax1.plot([], [], 'bo')
        self.mpl_canvas = self.fig.canvas
        self.add_widget(self.mpl_canvas)
        Clock.schedule_interval(self.update, 1)
   
    def on_data(self, *args):
        self.ax1.clear()
        y = [i**2 for i in self.data]
        self.ax1.plot(self.data, y, 'bo-', linewidth=5.0)
        self.mpl_canvas.draw_idle()
 
    def update(self, *args):
        self.data = random.sample(range(-10, 10), 5)

class DisplayApp(App):    
    def build(self):
        return build_string

    def process_file_path(self):
        file_path = self.root.ids.profile_screen.ids.input.text
        print("Filepath: " + file_path)
        if not os.path.exists(file_path):
            print("File doesn't exist.")
            # TODO: update UI with error
        else:
            if file_path.endswith('.csv'):
                pass
                # TODO:load file contents
            else:
                print("Filetype not supported. Use a properly formatted '.csv' file.")
                # TODO: update UI with error

    def read_data(Vref, Iin, Pout, Pmax):
        """
        read_data 
        Takes in system inputs and updates its data structure. Performs any calculations needed.

        """
        return

    def calculate_efficiency(self):
        """
        calculate_efficiency
        Determines two statistics: 
            - the % of the current supplied power to the max theoretical power
            - the % of cycles where the supplied power > x% diff from the max theoretical power
            - the avg number of cycles to get within a y% diff from the max theoretical power. Discounts events where the input conditions change faster than the avg number.
        """
        return

    def display_results(self):
        """
        display_results
        Runs the kivy widgets to display the data.
        """
        return
