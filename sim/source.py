"""
Source.py

Author: Matthew Yu, Array Lead (2020). 
Contact: matthewjkyu@gmail.com 
Created: 5/24/20 
Last Modified: 8/9/20 

Description: This file describes the Source class, which generates input values
for the Display and MPPT. The Source does not do any modelling, but it
aggregates the results of the cells.

Functionality: I should be able to do the following:
    - (setup) load from a configuration file or pass in an impulse or regime
        (the latter two are for single cell source modelling).
    - (iterate) able to step forward a cycle for all of the modules in the 
        source and return PV voltage and current.
    - (get_source_IV) able to return a full IV curve across all of the modules 
        in the source based on the current environmental conditions.
    - (get_source_gmpp) able to get the GMPP characteristics of the PV at the 
        current cycle.
    - (get_env_conditions) able to get the current environmental conditions 
        for all of the modules in the PV.
    - (get_model_type) able to get the current cell model name (i.e. nonideal, 
        ideal).
    - (set_current_cycle, increment_cycle) able to jump forward and rewind 
        back in time.

"""
from math import exp, pow, e
from numpy import log as ln
from cell import Cell
import json

SINGLE  = 1
DOUBLE  = 2
QUAD    = 4
OCT     = 8

MOD_NUM = 0
MOD_TYPE= 1
CELL    = 2

class Source:
    MAX_CURRENT = 100

    cycle = 0
    modules = []
    model_type = "Default"

    def __init__(self, model_type="Default"):
        """
        init
        Sets up the model type of the cell.

        Params:
            - model_type (String): type of model to represent the solar cell
                - [Nonideal]    (Single diode nonideal cell), default
                - Ideal         (Single diode ideal cell)
        
        Returns:
            - None
        """
        if model_type == "Ideal":
            self.model_type = "Ideal"
        else:
            self.model_type = "Nonideal"

    def setup(self, setup_type="", file_name="", regime=[], impulse=()):
        """
        setup Sets up an internal environmental regime either using an array of
        values, a file, or with initial conditions (an impulse).

        Args:
            - self
            - type      (String): Either "File", "Array", or "Impulse".
            - file_name (String): name of file in the `source_models` folder.
            - regime    ([[(int) Cycle, (float) Irradiance, (float) Temperature], ...]): Environmental regime.
            - impulse   (((float) Irradiance, (float) Temperature)): Impulse

        Return:
            - Whether the setup was successful (bool)

        Notes:
        - irradiance (float): light intensity on the cell (W/m^2)
        - temperature (float): surface temperature of the cell (C)
        - load (float): load on the system (W/s) NOTE: UNUSED

        # TODO: no support for load at the moment.
        """
        if setup_type == "":
            print("[CELL] WARN: Empty setup type -", setup_type)
            return False

        elif setup_type == "Array":
            if not regime:
                print("[CELL] WARN: Array setup type was selected, but regime is an empty list.")
                return False

            # create a single cell
            cell = Cell(self.model_type)
            self.modules.append((len(self.modules), SINGLE, cell))
            return cell.setup(setup_type, regime=regime)

        elif setup_type == "Impulse":
            if not impulse:
                print("[CELL] WARN: Impulse setup type was selected, but impulse is an empty tuple.")
                return False

            # create a single cell
            cell = Cell(self.model_type)
            self.modules.append((len(self.modules), SINGLE, cell))
            return cell.setup(setup_type, impulse=impulse)

        elif setup_type == "File":
            # TODO: check to see if we can find file
            with open("./source_models/" + file_name) as f:
                data = json.load(f)

                # get number of modules
                num_modules = int(data['num_modules'])

                # for each module, add a source object
                for module_index in range(0, num_modules):
                    module = data['pv_model'][module_index]

                    # get module type
                    module_type = 1
                    if module['module_type'] == "1x1":
                        module_type = SINGLE
                    elif module['module_type'] == '2x2':
                        module_type = QUAD
                    elif module['module_type'] == '2x4':
                        module_type = OCT
                    else:
                        module_type = SINGLE

                    cell = Cell(self.model_type)
                    self.modules.append((module_index, module_type, cell))
                    if module['env_type'] == "Array":
                        # early exit if one of the modules fail to build.
                        if not cell.setup(module['env_type'], regime=module['env_regime']):
                            return False
                    elif module['env_type'] == "Impulse":
                        if not cell.setup(module['env_type'], impulse=eval(module['env_regime'])):
                            return False
                    else:
                        print("[SOURCE] WARN: Invalid module type in file for module", module['module_num'])
                        return False
            
        else:
            print("[CELL] WARN: Invalid setup type -", setup_type)
            return False

    def iterate(self, v_in):
        """
        iterate Calculates the PV voltage and current the system should expect
        across a set of modules. If done in impulse mode, we take the current
        conditions, but if done in array mode, we take the passed in cycle and
        interpolate from the regime.

        Args:
            - v_in    (float): input voltage
            - cycle   (int): cycle to grab source data from

        Returns:
            - (v_out, i_out, irrad, temp, load) (tuple)

        # NOTE: This model is for Sunpower 1 cell at STD conditions
        """
        v_out_tot = 0.0
        i_out_tot = self.MAX_CURRENT

        # grab the last module's env. conditions; if we're testing a single cell
        # we can also use this.
        irrad = 0.0
        temp = 0.0
        load = 0.0
        for module in self.modules:
            (v_out, i_out, irrad, temp, load) = module[CELL].iterate(v_in)
            # simplistically, we just grab the total voltage and the lowest current.
            v_out_tot += v_out
            if i_out_tot > i_out:
                i_out_tot = i_out
        # TODO: add the effect of bypass diodes (essentially remove x volts for
        # TODO: every module based on y current)

        return (v_out, i_out, irrad, temp, load)

    def get_source_IV(self, step_size=.01):
        """
        TODO: figure this out
        get_source_IV 
        Returns an array of voltage and current values to display current
        solar panel IV pre-altered by the mppt.

        Args: 
            - step_size (float): step size. Defaults to .01 V.

        Returns: 
            - [[[[voltage, current]], gmpp], ...] (list of lists of lists)
                - gmpp: global maximum power point characteristics, [vmpp, impp, pmpp]
        """
        # for each module, get their IV curve, and search through the IV curve and grab the total voltage and min current for each cell voltage.
        characteristics = []
        for module in self.modules:
            characteristics.append(module[CELL].get_cell_IV(step_size))
        return characteristics

    def get_source_gmpp(self):
        """
        TODO: figure this out
        get_source_gmpp 
        Returns the global maximum power point parameters to be
        used by the simulation display. This is done by ...

        Returns: 
            - (vmpp, impp, pmpp) tuple of global maximum power point characteristics
        """
        characteristics = self.get_source_IV()
        # seek through the characteristics to find the max power and extract that
        return tuple(self.modules[0][CELL].get_cell_gmpp())
    
    def get_env_conditions(self):
        """
        get_env_conditions
        Returns source conditions for data analysis.

        Args:
            - None

        Returns:
            - [(irradiance, temperature, load), ...] (list of tuples)
        """
        env_conditions = [module[CELL].get_env_conditions() for module in self.modules]
        return env_conditions

    def get_model_type(self):
        """
        get_model_name
        Returns the name of the model.

        Args:
            - None
        Returns:
            - String name
        """
        return self.model_type

    def get_modules(self):
        """
        get_modules
        Returns the list of Modules.

        Args:
            - None
        Returns:
            - List (Cell)
        """
        return self.modules

    def set_current_cycle(self, cycle):
        """
        set_current_cycle 
        Sets the current cycle for all modules in the PV.

        Args:
            - cycle (int): current cycle for the PV modules.
        """
        for module in self.modules: 
            module[CELL].set_current_cycle(cycle)

    def increment_cycle(self):
        """
        increment_cycle 
        Increments the current cycle for all modules in the PV
        
        Returns:
            current cycle.
        """
        for module in self.modules: 
            module[CELL].increment_cycle()

        self.cycle += 1
        return self.cycle