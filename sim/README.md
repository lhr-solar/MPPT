# Python simulator for MPPT Algorithms

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
* pyqtgraph



## Feature Request and Bug list

* source
  * [x] source dependence on temperature
  * [x] source dependence on irradiance
  * [ ] <del>source dependence on load</del> remove source dependence on load - this is managed by the mppt
  * [ ] load profile from some formatted file (probably csv) TODO: priority
  * [ ] load source model from some formatted file
* dc-dc converter TODO: priority
  * [ ] research simulating a dc-dc converter that converts duty cycle to v_ref TODO: priority
* mppt
  * mppt_passthrough
    * [ ] Newton's method - stride approximation leads to strong mppt oscillation
    * [ ] Piegari (Optimal) - needs to develop an accurate model function for best voltage
  * mppt_other
    * [x] PandO
    * [x] PandO variable
    * [x] dP dV feedback control mppt algo
    * [ ] fuzzy logic mppt algo
    * [ ] ripple correlation control mppt algo
    * [x] update program structure to implement default method for each mppt algorithm, then give the option of using fixed and/or optimal.
  * [ ] modify simulation to match mppt hardware convert mppt v_ref to duty cycle
* simulation
  * [ ] Profile mode: mppt power is greater than max array power by a cycle
  * [x] Save to file
* optimization
  * [x] since the model is monotonically decreasing, swap from linear search to ternary search
  * [ ] have a hashed model (perhaps loaded from a file?) of a complete IV curve for all quantized values of temperature and irradiance. Additionally, perhaps use interpolation to get curve values if temp/irrad entry does not exist.
* upgrade
  * [ ] consider the feasibility of rewriting this application in rust or C++, as there may be extensive overhead computation as source models get more expensive. **LONG TERM**

## Papers and sites I haven't used yet but are promising

[Modeling Solar Cells](https://sites.google.com/site/banuphotovoltaic/pv/pv-arrays)

[Irradiance and PV Performance Optimization](e-education.psu.edu/ae868/node/877)

[Factors affecting PV Performance](file:///home/matthew/Downloads/FactorsAffectingPVperformance.pdf)

[Maxeon Gen II Solar Cells](file:///home/matthew/Documents/Uni/UTSVT/sp-gen3-solar-cell-ds-en-a4-160-507816f.pdf)

[Exploration of MPPT Algorithms](https://web.wpi.edu/Pubs/E-project/Available/E-project-030617-131157/unrestricted/AN_EXPLORATION_OF_MAXIMUM_POWER_POINT_TRACKING_ALGORITHMS.pdf)

[PandO with confined search space](https://www.sciencedirect.com/science/article/pii/S101836391730380X)

[PandO](http://www.actapress.com/Abstract.aspx?paperId=23133)

[Analysis and Optimization of maximum power point tracking algorithms in the presence of noise (Latham et al.)](https://cpb-us-e1.wpmucdn.com/sites.dartmouth.edu/dist/f/1307/files/2017/06/Analysis-and-Optimization-of-Maximum-Power-Point-Tracking-Algorithms-in-the-Presence-of-Noise-qc3ej8.pdf)

[Gradient Descent, possibly on power transformation](https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote07.html)

[A new maximum power point control algorithm of photovoltaic generation system (Bian et al.)](https://www.tandfonline.com/doi/full/10.1080/21642583.2018.1558419)

[On global extrmum seeking in the presence of local extrema](https://www-sciencedirect-com.ezproxy.lib.utexas.edu/science/article/pii/S0005109808004147)

[Advances in solar photovoltaic power plants (Islam et al.)](https://books.google.com/books?id=nPh6DAAAQBAJ&pg=PA91&lpg=PA91&dq=discrete+newton+method+mppt&source=bl&ots=qXRTL0UCqg&sig=ACfU3U2qzhM4SR83wCpQYoiPg1QgVhoQ-g&hl=en&sa=X&ved=2ahUKEwjjt6W69dnpAhUJa80KHVs1ACkQ6AEwB3oECAwQAQ#v=onepage&q=discrete%20newton%20method%20mppt&f=false)

[Accurate Simulation of MPPT Methods Performance When Applied to Commercial Photovoltaic Panels (Cubas et al.)](https://www.hindawi.com/journals/tswj/2015/914212/)