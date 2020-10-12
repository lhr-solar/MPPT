#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "../dep/doctest.h"
#include "Filter/MedianFilter.h"
#include <cmath>

TEST_CASE("Testing the Median filter.") {
    MedianFilter f = MedianFilter(5);

    SUBCASE("Read while empty.") {
        CHECK(f.getResult() == 0);
    }

    SUBCASE("Read after write.") {
        f.addSample(10.0);
        CHECK(f.getResult() == 10.0);
    }

    SUBCASE("Read after a bunch of writes.") {
        double expected_res[20] = {
            100,
            55,
            20,
            25,
            30,
            30,
            40,
            60,
            70,
            80,
            80,
            90,
            100,
            110,
            120,
            120,
            130,
            140,
            160,
            170
        };
        // add 20 samples, increasing linearly by 10, and then some noisy 100s every 5 cycles.
        for (int i = 0; i < 20; i++) {
            if (i%5 == 0) { f.addSample(100); }
            else { f.addSample(i*10.0); }

            // assert the expected filter output at every point
            CHECK(std::trunc(f.getResult() * 100.0) / 100.0 == expected_res[i]);
        }
    }
}
