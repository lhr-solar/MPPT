# Python simulator for MPPT Algorithms.
Created on 5/24/20 by Matthew Yu, Solar Array Lead (2020) of the UT Solar Vehicles Team.

*Consider making an actual structured repo, Matthew.*
[Repo Structure](https://docs.python-guide.org/writing/structure/)

## Dependencies
* python3
* sys
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
- [x] input parameters


Modeling Solar Cells
https://sites.google.com/site/banuphotovoltaic/pv/pv-arrays
Irradiance and PV Performance Optimization
e-education.psu.edu/ae868/node/877
Factors affecting PV Performance
file:///home/matthew/Downloads/FactorsAffectingPVperformance.pdf

Maxeon Gen II Solar Cells
file:///home/matthew/Documents/Uni/UTSVT/sp-gen3-solar-cell-ds-en-a4-160-507816f.pdf

Exploration of MPPT Algorithms
https://web.wpi.edu/Pubs/E-project/Available/E-project-030617-131157/unrestricted/AN_EXPLORATION_OF_MAXIMUM_POWER_POINT_TRACKING_ALGORITHMS.pdf



PandO with confined search space
https://www.sciencedirect.com/science/article/pii/S101836391730380X
PandO
http://www.actapress.com/Abstract.aspx?paperId=23133