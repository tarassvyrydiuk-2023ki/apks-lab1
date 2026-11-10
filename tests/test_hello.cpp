#include <gtest/gtest.h>

#include <string>

#include "hello/hello.hpp"

TEST(HelloTest, BasicAddition) {
    EXPECT_DOUBLE_EQ(hello::add(2, 3), 5);
}

TEST(HelloTest, AdditionWithNegativesAndZero) {
    EXPECT_DOUBLE_EQ(hello::add(0, 0), 0);
    EXPECT_DOUBLE_EQ(hello::add(-1, 1), 0);
    EXPECT_DOUBLE_EQ(hello::add(2.5, 0.5), 3.0);
}

TEST(HelloTest, Greeting) {
    EXPECT_EQ(hello::greeting(), std::string("Hello, World!"));
}
