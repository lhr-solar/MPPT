# Python simulator for MPPT Algorithms.
Created on 5/24/20 by Matthew Yu, Solar Array Lead (2020) of the UT Solar Vehicles Team.

*Consider making an actual structured repo, Matthew.*
[Repo Structure](https://docs.python-guide.org/writing/structure/)

## Dependencies
* matplotlib
* numpy
* bisect
* math

## Feature Request
- [x] source dependence on temperature
- [ ] source dependence on irradiance
- [ ] source dependence on load
- [ ] load from some formatted file (probably csv)
- [x] dP dV feedback control mppt algo
- [ ] fuzzy logic mppt algo
- [ ] ripple correlation control mppt algo
- [ ] modify simulation to match mppt hardware convert mppt v_ref to duty cycle and create a dc to dc converter that'll convert duty cycle to v_ref