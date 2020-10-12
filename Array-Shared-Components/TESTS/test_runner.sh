BUILD_ROOT="BUILD/"
SRC_ROOT="../src/"
# TODO: STATIC_LIB_PATH="../BUILD/libraries/Array-Shared-Components/NUCLEO_L432KC/GCC_ARM/"


# Delete everything in the BUILD directory.
rm BUILD/* -rf

# Auto generate test executables

# This find command checks for all files called test_*
# in the TESTS folder, recursively. For each file that's
# found, make a new directory for it in BUILD, if it doesn't
# exist, and then compile the executable there and run it.
find . -name "test_*.cpp" | while read file;
do
    echo "Generating test for $file.";

    # Extracting the directory and file name metadata.
    DIR=${file%/*}
    FILE=${file%.*}

    # Build the directory if it exists (-p flag).
    mkdir -p ${BUILD_ROOT}${DIR}

    # Have a separate option compiling any cpp files if they exist in the source.
    echo "Searching for $SRC_ROOT$DIR/*.cpp"
    count=`ls -1 ${SRC_ROOT}${DIR}/*.cpp 2>/dev/null | wc -l`

    # Make the executable and place it in the new directory.
    # We do a couple of things here:
    #   -Wall : Turns on a bunch of warnings.
    #   -Wextra : Even more warnings.
    #   -o : Specifies the name and location of our executable.
    #   -I : Specifies a directory to be added to be searched for header files.
    #   The last two arguments are the file to compile with the main, as well
    #   as all the files in the library added.
    if [ $count != 0 ]; then
        g++ -Wall -Wextra                                       \
            -o ${BUILD_ROOT}${FILE}                             \
            -I ./dep -I ${SRC_ROOT}                             \
            ${SRC_ROOT}${DIR}/*.cpp                             \
            ${file}                                             ;
    else
        g++ -Wall -Wextra                                       \
            -o ${BUILD_ROOT}${FILE}                             \
            -I ./dep -I ${SRC_ROOT}                             \
            ${file}                                             ;
    fi

    While we're at it, let's execute it as well.
    if [ -f ${BUILD_ROOT}${FILE} ]
    then
        echo "Executing testbench:";
        # Executing the executable we generated.
        ./${BUILD_ROOT}${FILE};
    else
        echo "Didn't find an executable.";
    fi

    echo "$file test Generated.";
    echo "\n\n";
done

        # -I ../mbed-os/platform/include/                     \
        # -I ../mbed-os/targets/TARGET_STM/                   \
        # -I ../mbed-os/targets/TARGET_STM/TARGET_STM32L4/    \
        # -I ../mbed-os/targets/TARGET_STM/TARGET_STM32L4/device/ \
        # -I ../mbed-os/targets/TARGET_STM/TARGET_STM32L4/TARGET_STM32L432xC/ \
        # -I ../mbed-os/targets/TARGET_STM/TARGET_STM32L4/TARGET_STM32L432xC/device/  \
        # -I ../mbed-os/targets/TARGET_STM/TARGET_STM32L4/TARGET_STM32L432xC/TARGET_NUCLEO_L432KC/    \
        # -I ../mbed-os/platform/include/platform/            \
        # -I ../mbed-os/cmsis/CMSIS_5/CMSIS/TARGET_CORTEX_M/Include/ \
        # -I ../mbed-os/drivers/include/                      \
        # -I ../mbed-os/hal/include/                          \
        # -I ../mbed-os/platform/cxxsupport/                  \
        # -D STM32L432xx                                      \

        # -L ${STATIC_LIB_PATH}libArray-Shared-Components.a   ;
    # TODO: 'I {MBED_ROOT}'' figure out how to include mbed.h dependency
    # TODO: '${SRC_ROOT}${DIR}/*.cpp' figure  out how to include option for building libraries
