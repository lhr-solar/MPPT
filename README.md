# MPPT

Repo containing working code for the UTSVT MPPT and array simulation.

### Run Simulator

Navigate to the simulator directory with `cd sim` (assuming you are at the root folder of the repo.)
To install dependencies, run `pip3 install -r requirements.txt`.
To run the MPPT Simulator, call `python3 main.py`.
To run the Solar cell model Simulator, call `python3 source_main.py`.

### Development Instructions

Checkout a feature branch with the naming convention `NAME#ISSUE`. For example,
`myu#23`. This indicates that this branch should contain code for the feature
issue #23, `Adding some sample smoothing for the sensor class`. After checking
out the branch, make your necessary edits with the code and at completion, file
a PR to `master`. The repo maintainer (Matthew Yu) will review the code and
approve and merge it.

Best practices include committing to the branch after every milestone in
development; this is up to the user to define the milestones. For example, for
the above issue, an example set of milestones may be:

- Sample smoothing API function written and parameter added to constructor in
  the header file.
- Implementation of sample smoothing completed in .cpp.
- Adjustment of main file to use the new API.

Additionally, when working with python code, we recommend the use of the [black
autoformatter](https://medium.com/@marcobelo/setting-up-python-black-on-visual-studio-code-5318eba4cd00).
This will ensure consistent code for commits.
