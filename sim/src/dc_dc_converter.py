"""
dc_dc_converter.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 9/22/20
Last Modified: 9/22/20
Description: Specifies the implementation of a DC to DC converter simulation component.
"""


class DCDCConverter:
    def __init__(self):
        self.pulse_width = 0.0

    def setup(self, array_voltage=0.0, load_voltage=0.6):
        """
        setup
        sets up initial values for the dc-dc converter.

        Args:
            - array_voltage (float): expected array output voltage.
            - load_voltage  (float): initial load voltage. Battery in the case
            of the array.

        Returns:
            - None
        """
        self.array_voltage = array_voltage
        self.load_voltage = load_voltage

    def set_pulse_width(self, mppt_target_voltage):
        """
        set_pulse_width
        generates a pulse width from an expected target voltage based on the
        load voltage.

        Args:
            - mppt_target_voltage (float): expected array output voltage after
            inputting a specific pulse width.

        Returns:
            - None
        """
        if mppt_target_voltage > 0.0:
            self.pulse_width = 1 - self.load_voltage / mppt_target_voltage
            self.array_voltage = mppt_target_voltage

    def set_load_voltage(self, load_voltage):
        """
        set_load_voltage
        updates the load voltage for dc-dc converter calculation.
        Typically static in the current model.

        Args:
            - None

        Returns:
            - None
        """
        self.load_voltage = load_voltage

    def get_pulse_width(self):
        """
        get_pulse_width
        gets the current pulse width as a fraction from [0, 1].

        Args:
            - None

        Returns:
            - float: pulse width
        """
        return self.pulse_width

    def get_voltage_out(self):
        """
        get_voltage_out
        gets the expected array voltage given the current pulse width.
        Reverse of set_pulse_width - this is what we expect the dc-dc converter to return

        Args:
            - None

        Returns:
            - float: expected array voltage
        """
        return self.array_voltage
