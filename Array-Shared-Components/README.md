# Array-Shared-Components

Holds shared code between the MPPT and Curve Tracer projects.
Instructions were written in particular for linux users in mind.

The repo structure is as follows:

- BUILD: An empty folder where output of your MBED builds be generated.
- TESTS: Testbenches for classes go into here. Also has a BUILD subfolder for
  test result generation.

---

## Requirements

- [doctest](https://github.com/onqtam/doctest) (Header is inserted into
  `TESTS/dep` by default.)
- GCC 6+
- Bash 4.4+
- Python 2.7.x or 3.5+
- Pip 10.0+
- Mbed CLI 1.8.0+

---

## Writing Code and Contributing

If you are making modifications to existing code in this codebase (i.e. editing
the implementation of `src/Filter/MedianFilter.h`), make sure you run the steps in
**TESTING** prior to committing.

If you're writing new code for this codebase, the folder should be in the `src` folder
and in CamelCase, no spaces or dashes. (i.e. say a new class folder called dc-dc
converter should be called `src/DCDCConverter`.)

All you really need is the header and implementation file. Derived classes can
be in the same folder. See `src/Filter` as an example of this.

---

## Testing

### Writing Tests

After writing your potential driver, you need to write unit tests for this to
make sure it functions appropriately. Make a new folder in `/TESTS` with the
same naming convention as before (i.e. `/TESTS/DCDCConverter`), and then a file named `test_<CLASS>.cpp` for
every class you need to test.

We're using
[DocTest](https://github.com/onqtam/doctest/blob/master/doc/markdown/tutorial.md)
to do unit testing; follow one of the other tests for syntax help or take a decent
look at the tutorial link. Suggested sections are [A simple
example](https://github.com/onqtam/doctest/blob/master/doc/markdown/tutorial.md#a-simple-example),
[Test cases and
subcases](https://github.com/onqtam/doctest/blob/master/doc/markdown/tutorial.md#test-cases-and-subcases),
and the [Reference](https://github.com/onqtam/doctest/blob/master/doc/markdown/readme.md#reference)(s).

### Running Tests

To run the tests, navigate to the `/TEST` folder.
Call the following command:

```bash
sh test_runner.sh
```

You should see output like the following:

```bash
sh test_runner.sh
Generating test for ./Example/test_TestClass.cpp.
/tmp/ccftzVt0.o: In function `_DOCTEST_ANON_FUNC_8()':
test_TestClass.cpp:(.text+0x130d5): undefined reference to `TestClass::hi()'
collect2: error: ld returned 1 exit status
Didn't find an executable.
./Example/test_TestClass.cpp test Generated.



Generating test for ./Sensor/test_Sensor.cpp.
/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/Scrt1.o: In function `_start':
(.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status
Didn't find an executable.
./Sensor/test_Sensor.cpp test Generated.



Generating test for ./Filter/test_Filter.cpp.
Executing testbench:
[doctest] doctest version is "2.4.0"
[doctest] run with "--help" for options
===============================================================================
[doctest] test cases:      1 |      1 passed |      0 failed |      0 skipped
[doctest] assertions:      3 |      3 passed |      0 failed |
[doctest] Status: SUCCESS!
./Filter/test_Filter.cpp test Generated.



Generating test for ./Filter/test_SMAFilter.cpp.
Executing testbench:
[doctest] doctest version is "2.4.0"
[doctest] run with "--help" for options
===============================================================================
[doctest] test cases:      1 |      1 passed |      0 failed |      0 skipped
[doctest] assertions:     22 |     22 passed |      0 failed |
[doctest] Status: SUCCESS!
./Filter/test_SMAFilter.cpp test Generated.



Generating test for ./Filter/test_MedianFilter.cpp.
Executing testbench:
[doctest] doctest version is "2.4.0"
[doctest] run with "--help" for options
===============================================================================
[doctest] test cases:      1 |      1 passed |      0 failed |      0 skipped
[doctest] assertions:     22 |     22 passed |      0 failed |
[doctest] Status: SUCCESS!
./Filter/test_MedianFilter.cpp test Generated.

```

The test_runner script will automatically compile your tests for you and execute
them so you can quickly and easily see the results.

You can also re run the individual executables from the `TESTS/BUILD` folder; it
should be organized with the same structure as the folders in `TESTS` or `src`.

Running the executable can be as simple as (assuming you're in the root
directory) the following: `./TESTS/BUILD/Filter/test_Filter` .

The development process can be as easy as making changes to your code and
testbench, running the script, making fixes, and repeat!

I highly suggest learning how to TDD, or Test Driven Development. A couple of
links are provided below:
- [Test-driven development and unit testing with examples in C++ (alexott.net)](http://alexott.net/en/cpp/CppTestingIntro.html)
- [Test-driven development (wikipedia)](https://en.wikipedia.org/wiki/Test-driven_development)
- [5 steps of test-driven development (IBM)](https://developer.ibm.com/articles/5-steps-of-test-driven-development/)

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
