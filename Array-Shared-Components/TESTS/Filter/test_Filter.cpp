#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "../dep/doctest.h"
#include "Filter/Filter.h"


TEST_CASE("Testing the passthrough filter.") {
    Filter f = Filter();

    SUBCASE("Read while empty.") {
        CHECK(f.getResult() == 0);
    }

    SUBCASE("Read after write.") {
        f.addSample(10.0);
        CHECK(f.getResult() == 10.0);
    }

    SUBCASE("Read after a bunch of writes.") {
        for (int i = 0; i < 20; i++) {
            f.addSample(1.0);
        }
        f.addSample(10.0);
        CHECK(f.getResult() == 10.0);
    }

    f.shutdown();
}