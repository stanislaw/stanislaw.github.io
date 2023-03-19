---
layout: post
title: "Using mutation testing score to measure a
reliability of a single function"
date: 2017-05-05 19:20:00 +0200
keywords: "testing, mutation testing, mull, software reliability"
description: "This post describes interesting and unusual application of mutation testing method to a single function, not to a whole project."
---

[Mull project](https://github.com/mull-project/mull) is slowly transforming
from an early-stage research project to a tool that allows us to do a
mutation testing analysis on real-world projects.
As we develop Mull further and apply mutation testing to different projects,
we learn more about a behavior of a code and a test code.

This post describes interesting and unusual application of mutation testing
method to a single function, not to a whole project.

In mutation testing theory there is a concept of "mutation score" which is defined
as:

    mutation score = number of mutants killed / total number of mutants

Mutation testing aims at achieving 100% mutation score on a codebase because this
100% means that code's tests are so good that they can detect all of
the possible mutations that can be applied to that code. See [Mutation Testing](https://en.wikipedia.org/wiki/Mutation_testing) on Wikipedia where this is fully explained.

Let's now think about what mutation score means for a single function. Let's
consider a function and with one test for it:

    static int algorithm(int a, int b) {
      ...
      return result
    }

    TEST(algorithm, calculates) {
      ASSERT_EQ(algorithm(2, 3), 5);
    }

Let's imagine that we have run a mutation testing tool on this one test and got
10 mutants generated with a mutation score of 50%. Obviously, in this simple
example, these 10 mutations were generated somewhere in `algorithm` function.
Our test failed on 5 mutations (these 5 "mutants were killed") and passed on
the other 5 mutations (these 5 "mutants were not killed").

If we think for a moment that each of these 10 mutations can substitute for some
real-world problem like a hardware error, cosmic rays, malevolent interference,
then we can read this mutation score as the following:

<b>mutation score of 50% for 10 mutations in 1 function => 10 different bad things can happen to this function and 5 of these will make the final result incorrect.</b>

Let's pretend that we do want our function to work somewhere where having
the result of this function correct is super-critical. Then mutation score
becomes an interesting metric that we can use to evaluate how reliable our
function is:

<b>if we can write our function in a way that mutation testing applied to its
tests will always produce a mutation score of 0%, then we can consider our
function tolerant to these errors.</b>

Of course, the number of errors that we can simulate is limited by a number
of mutation operators that a particular tool supports. In our case Mull supports

- `AddMutation`, replaces "+" with "-"
- `NegateCondition`, replaces "true" with "false", "==" with "!=", "<" with ">=", etc
- `RemoveVoidFunctionCall`, if your function has a `callToSomeVoidFunction()`,
this call is simply removed.

Given this very limited number of mutation operators let's write such a
function that would give us a mutation score of 0%.

### Step 1: Original algorithm with mutation score: 100%

    #include "gtest/gtest.h"

    static int safeAlgorithm(int a, int b) {
      return a + b;
    }

    TEST(safeAlgorithm, calculates) {
      ASSERT_EQ(safeAlgorithm(2, 3), 5);
    }

If we run Mull against this code, it finds only one mutation point:
`AddMutation` operator which for `a + b` expression generates a mutation `a - b`:

    return a + b;
             ^

Final report contains 1 mutation which is killed by `safeAlgorithm.calculates`
test:

    Note: Google Test filter = safeAlgorithm.calculates
    [==========] Running 1 test from 1 test case.
    [----------] Global test environment set-up.
    [----------] 1 test from safeAlgorithm
    [ RUN      ] safeAlgorithm.calculates
    /usr/local/mull/mull/unbreakable/unbreakable.cpp:8: Failure
        Expected: safeAlgorithm(2, 3)
        Which is: -1
    To be equal to: 5
    [  FAILED  ] safeAlgorithm.calculates (0 ms)
    [----------] 1 test from safeAlgorithm (0 ms total)
    [----------] Global test environment tear-down
    [==========] 1 test from 1 test case ran. (0 ms total)
    [ PASSED ] 0 tests.
    [ FAILED ] 1 test, listed below:
    [ FAILED ] safeAlgorithm.calculates

    1 FAILED TEST

### Step 1: mutation testing report

<img src="/images/2017-05-05-unbreakable/Unbreakable_1.png"/>

### Step 2: Improved algorithm with mutation score: 0%

Obviously, we cannot use the original algorithm code as is because `AddMutation`
will break it and we will not have a valid result of the algorithm. In my solution
I found that I had to introduce a redundancy: 3 versions of the same algorithm
located in different functions so that `AddMutation` can only break one of them.
The number 3 comes from a minimal number of 2 required for "consensus": to decide
on which 2 of 3 algorithms work as expected.

    #include "gtest/gtest.h"

    static int algorithm1(int a, int b) {
      return a + b;
    }

    static int algorithm2(int a, int b) {
      return a + b;
    }

    static int algorithm3(int a, int b) {
      return a + b;
    }

    static bool safeAlgorithm(int a, int b, int *result) {
      int alg1 = algorithm1(a, b);
      int alg2 = algorithm2(a, b);
      int alg3 = algorithm3(a, b);

      if (alg1 == alg2) {
        if (result) {
          *result = alg1;
        }
        return true;
      }

      if (alg2 == alg3) {
        if (result) {
          *result = alg2;
        }
        return true;
      }

      if (alg1 == alg3) {
        if (result) {
          *result = alg1;
        }
        return true;
      }

      return false;
    }

    TEST(safeAlgorithm, calculates) {
      int a = 2;
      int b = 3;

      int result = 0;
      bool success = safeAlgorithm(a, b, &result);

      ASSERT_TRUE(success);
      ASSERT_EQ(result, 5);
    }

### Step 2: mutation testing report

<img src="/images/2017-05-05-unbreakable/Unbreakable_2.png"/>

### Observations

- Mull currently only supports 3 mutation operators: `AddMutation`,
`RemoveVoidFunctionCall`, `NegateCondition`. We saw that only
`AddMutation` and `NegateCondition` contributed to the mutations. When Mull
supports more mutation operators, this code will no longer have a mutation score
of 0% because more mutations will find a way to fail the test.

- Only single mutations were applied. The code would be very different if we
applied combinations of 2 and more mutations.

### Conclusion

Using mutation testing score as a metric for a reliability of a single function is
an interesting application of mutation testing tool. I am looking forward
to running Mull on this code when Mull supports much more mutation operators
than it supports currently.

I would be happy to learn about your experience with writing unbreakable
functions or if you know if there are any white papers about attempts to measure a reliability
of a source code. Feel free to [drop me a line](mailto:s.pankevich@gmail.com).

See full reports here:

- [Mutation testing report for step 1](/files/2017-05-05-unbreakable/Unbreakable_1.zip)
- [Mutation testing report for step 2](/files/2017-05-05-unbreakable/Unbreakable_2.zip)
