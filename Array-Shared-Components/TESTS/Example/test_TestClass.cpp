#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "../dep/doctest.h"
#include "Example/TestClass.h"


TEST_CASE("A trivial test.") {
    CHECK(TestClass::hi() == 2);
}