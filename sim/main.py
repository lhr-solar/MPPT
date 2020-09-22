"""
main.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 5/24/20
Last Modified: 8/22/20
Description: This is the main handler for the mppt simulator. 
    The simulator has three main components:
      1. Source simulator - The program simulates a solar cell or set of solar cells by taking in static parameters or a datafile of input values over time.
      2. MPPT Algorithm - A black box that manages algorithms (PandO, Incr. Conduction, RCC, Fuzzy Logic, etc) to maximize power on the load.
      3. Simulator - The outputs of the MPPT and the source are calculated, stored, and graphed. Data over time will be evaluated to determine and compare efficiencies between algorithms.
"""
import sys
import time

from src.dc_dc_converter import DCDCConverter
from src.source import Source
from src.simulation import Simulation

from src.mppt_algorithms.mppt_perturb_and_observe import PandO
from src.mppt_algorithms.mppt_incremental_conduction import IC

# from src.mppt_algorithms.mppt_ripple_correlation_control import RCC
# from src.mppt_algorithms.mppt_fuzzy_logic import FL
from src.mppt_algorithms.mppt_dP_dV_feedback_control import FC
from src.mppt_algorithms.mppt_passthrough import PT

from regime import env_regime


def main():
    profile_file_path = ""
    mode_profile = False

    # NOTE: Modify these values
    max_cycle = 200
    refresh_rate = 60  # FPS
    sample_rate = 1
    stride = 0.05
    v_ref = 0
    stride_mode = None
    use_file = True

    # --------------PARAMETER PROMPTS--------------
    # source input dialogue
    string_source_model_type = input(
        "Source Model type (see src docs): ['Nonideal']|'Ideal': "
    )

    # MPPT input dialogue
    mppt = None
    string_mppt_algorithm_type = input(
        "MPPT Algorithm type: ['PandO']|'IC'|'FC'|'Passthrough': "
    )
    if string_mppt_algorithm_type == "IC":
        mppt = IC()
    elif string_mppt_algorithm_type == "FC":
        mppt = FC()
    elif string_mppt_algorithm_type == "Passthrough":
        mppt = PT()
    else:
        mppt = PandO()
    # mppt stride mode dialogue
    if string_mppt_algorithm_type == "Passthrough":
        string_stride_mode = input(
            "Stride mode for MPPT (see src docs): ['Golden']|'Ternary'|'Bisection'|'Newton(X)'|'BFGS(X)': "
        )
        if (
            string_stride_mode == "Golden"
            or string_stride_mode == "Ternary"
            or string_stride_mode == "Bisection"
            or string_stride_mode == "Newton"
            or string_stride_mode == "BFGS"
        ):
            stride_mode = string_stride_mode
    else:
        string_stride_mode = input(
            "Stride mode for MPPT (see src docs): ['Fixed']|'Adaptive'|'Optimal': "
        )
        if (
            string_stride_mode == "Fixed"
            or string_stride_mode == "Optimal"
            or string_stride_mode == "Adaptive"
        ):
            stride_mode = string_stride_mode

    # profile input dialogue
    string_profile = input("Profile ['impulse']|'profile'|'file': ")
    if string_profile == "profile":
        mode_profile = True
    if string_profile == "file":
        string_file_path = input("Enter file name (i.e. 'single_cell.json'): ")
        profile_file_path = string_file_path
        mode_profile = True

    # use file
    string_use_file = input(
        "Use cached model or from scratch: ['file']|'scratch':"
    )
    if string_use_file == "scratch":
        use_file = False

    # max simulation cycle
    string_max_cycle = input("Max cycle ['" + str(max_cycle) + "']: ")
    try:
        tmp_max_cycle = int(string_max_cycle)
        max_cycle = tmp_max_cycle
    except ValueError:
        print("Invalid integer. Defaulting to", max_cycle, "cycles.")
    # simulation sample rate
    string_sample_rate = input("Sample rate ['" + str(sample_rate) + "']: ")
    try:
        tmp_sample_rate = int(string_sample_rate)
        sample_rate = tmp_sample_rate
    except ValueError:
        print(
            "Invalid integer. Defaulting to a sample every "
            + str(sample_rate)
            + " cycles."
        )
    # simulation starting reference voltage
    string_v_ref = input(
        "Starting mppt output voltage ['" + str(v_ref) + "']: "
    )
    try:
        tmp_v_ref = float(string_v_ref)
        v_ref = tmp_v_ref
    except ValueError:
        print(
            "Invalid integer. Defaulting to a cycle 0 v_ref of "
            + str(v_ref)
            + " V."
        )
    # simulation stride
    string_stride = input(
        "Default stride (for fixed stride function) ['" + str(stride) + "']: "
    )
    try:
        tmp_stride = float(string_stride)
        stride = tmp_stride
    except ValueError:
        print("Invalid integer. Defaulting to stride of " + str(stride) + ".")

    # initialization
    converter = DCDCConverter()
    source = Source(string_source_model_type, use_file=use_file)
    simulation = Simulation(mppt.get_name())

    # -------------- SIMULATION START --------------
    # simulating from a dataset
    if mode_profile is True:
        print("Running in Profile mode.")
        input("Ready to start. Press enter to run the simulation.")

        cycle_start = 0
        time_step = 1
        # mppt
        v_mppt = 0
        i_mppt = 0

        if profile_file_path != "":
            source.setup("File", file_name=profile_file_path)
        else:
            source.setup("Array", regime=env_regime)
        mppt.setup(v_ref, stride, sample_rate, stride_mode)
        converter.setup(v_ref, 0.6)
        simulation.init_display(0, cycle_start, max_cycle, time_step)

        main_loop(
            source,
            mppt,
            converter,
            simulation,
            cycle_start,
            max_cycle,
            time_step,
            refresh_rate,
            v_ref,
        )

    # simulating from an impulse created by the user
    else:
        print("Running in Impulse mode.")

        # for source and simulation
        irradiance = 1000
        temperature = 25
        load = 0
        cycle_start = 0
        time_step = 1
        # mppt
        v_mppt = 0
        i_mppt = 0

        string_irrad = input(
            "Starting irradiance ['" + str(irradiance) + "']: "
        )
        try:
            tmp_irrad = float(string_irrad)
            irradiance = tmp_irrad
        except ValueError:
            print(
                "Invalid integer. Defaulting to an irradiance of "
                + str(irradiance)
                + " W/m^2."
            )

        string_temp = input(
            "Starting temperature ['" + str(temperature) + "']: "
        )
        try:
            tmp_temp = float(string_temp)
            temperature = tmp_temp
        except ValueError:
            print(
                "Invalid integer. Defaulting to a temperature of "
                + str(temperature)
                + " C."
            )

        string_load = input("Starting load ['" + str(load) + "']: ")
        try:
            tmp_load = float(string_load)
            load = tmp_load
        except ValueError:
            print(
                "Invalid integer. Defaulting to a load of " + str(load) + " W."
            )

        input("Ready to start. Press enter to run the simulation.")

        source.setup("Impulse", impulse=(irradiance, temperature))
        mppt.setup(v_ref, stride, sample_rate, stride_mode)
        converter.setup(v_ref, 0.6)
        simulation.init_display()

        main_loop(
            source,
            mppt,
            converter,
            simulation,
            cycle_start,
            max_cycle,
            time_step,
            refresh_rate,
            v_ref,
        )


def main_loop(
    source,
    mppt,
    converter,
    simulation,
    cycle_start,
    max_cycle,
    time_step,
    refresh_rate,
    v_ref,
):
    cycle = 0

    while cycle <= max_cycle:  # simulator main loop
        if cycle % 20 == 0:
            print("\nCycle: " + str(cycle))

        # get source power point
        (characteristics, (v_mpp, i_mpp, p_mpp)) = source.get_source_IV()
        # get new values with the existing source after applying reference voltage
        (v_out, i_out, irrad, temp, load) = source.iterate(v_ref)
        # update Simulation
        simulation.add_datapoint(
            cycle,
            (irrad, temp, load),
            (characteristics, (v_mpp, i_mpp, p_mpp)),
            (v_out, i_out, v_out * i_out),
        )
        simulation.update_display(cycle_start, max_cycle, time_step)
        time.sleep(1 / refresh_rate)
        # pipe source into the mppt to find the new v_ref
        v_ref = mppt.iterate(v_out, i_out, temp, cycle)
        # pipe mppt estimate into the dc-dc-converter
        converter.set_pulse_width(v_ref)
        v_ref = converter.get_voltage_out()

        # update cycle
        cycle = source.increment_cycle()

        # impulse update parameters here
        # irradiance += UPDATE_HERE
        # temperature += .5
        # load += UPDATE_HERE
        # source.setup_i(irradiance, temperature, load)

    input("Halted at the end of cycle " + str(max_cycle))


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    main()
else:
    print("Run main.py as a script.")
