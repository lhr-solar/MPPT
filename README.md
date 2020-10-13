# MPPT

Code for the UTSVT Maximum Power Point Trackers to be implemented on the STM32
NUCLEO L432KC.

---

## MPPT Board Software

Located in the `MPPT/` root folder.
The relevant file structure is as follows:

```bash
MPPT/
  |-- Array-Shared-Components/
  |     |-- src/
  |         |-- CANDevice/
  |         |-- Filter/
  |         |-- Sensor/
  |         |-- Serial/
  |-- dcdcconverter/
  |-- mppt/
  |-- main.cpp
```

For reference, code developed by the senior design teams were last present in
commit 2c36e87d72c7dfa2e403e846bccae883f6e5aa30.
To access, try `git checkout 2c36e87d72c7dfa2e403e846bccae883f6e5aa30`.

---

## Development Instructions

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

We don't have an explicit style guide for C/C++ code, but you can generally take
a look at some of the files we have to get a feel for it. For example, check
`MPPT/mppt/mppt.h` and `MPPT/mppt/mppt.cpp`.

---

## Building

Note that you need to set up the repo as an mbed project. Instructions on how to
install mbed-cli can be found
[here](https://os.mbed.com/docs/mbed-os/v6.3/build-tools/mbed-cli.html). You can
do so to navigating to the root of this repo and calling

`mbed new .`

So far, the only build target these components were designed for in mind has
been the STM32 L432KC Nucleos. However, these should be cross-compatible with
other devices compatible with the mbed library.

Since there is no main here, to see if everything compiles correctly for our
target, run the following:

`mbed compile -m NUCLEO_L432KC -t GCC_ARM -c --library`

At the end you should see a build success message with the target.
