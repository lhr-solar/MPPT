import sys

from source import Source
from simulation import Simulation

from mppt_algorithms.mppt_perturb_and_observe import PandO
from mppt_algorithms.mppt_incremental_conduction import IC
# from mppt_algorithms.mppt_ripple_correlation_control import RCC
# from mppt_algorithms.mppt_fuzzy_logic import FL
from mppt_algorithms.mppt_dP_dV_feedback_control import FC
from mppt_algorithms.mppt_passthrough import PT

file = "source_models/single_cell.json"
regime = [
    [0, 1000, 25],
    [1, 1000, 50],
    [2, 1000, 75]
]

source = Source()
print(source.setup(setup_type="Impulse", file_name=file, regime=regime, impulse=(1000, 25)))
print(source.get_env_conditions())
source.set_current_cycle(1)
print(source.get_env_conditions())
source.set_current_cycle(2)
print(source.get_env_conditions())
print(source.get_modules())