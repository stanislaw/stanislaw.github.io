How to find the slowest XCTest
==============================

:date: 2016-08-04 19:05:00
:modified: 2016-08-04 19:05:00
:tags: Xcode, Testing
:category: Posts
:slug: 2016-08-04-how-to-find-the-slowest-xctest
:summary: A command-line snippet for finding the slowest XCTest.

We can distinguish between performance of different kinds of tests in the
context of iOS development: unit tests are expected to run very fast because
they should not touch any I/O do network calls or fire timers, integration tests
are slower since they involve I/O or network or interaction between multiple
components including external parties, acceptance tests are the slowest since a
whole system is under test. Functional or UI snapshot tests are somewhere in
between.

Whatever the tests you're working on, there might be room for improvements. The
following is simple but useful command based on ``awk`` that can help you to
identify the slowest tests in your XCTest-based test suite.

First, you need to get the output log produced by your XCTest-based test target
and store it to a file. You can either copy and paste the build log from Xcode,
after you have run ``Command + U``, or use the following command that runs
``xcodebuild test``:

.. code-block:: bash

    xcodebuild -project YourProject.xcodeproj \
               -scheme YourProject \
               -destination 'platform=iOS Simulator,name=iPhone 6s Plus,OS=9.3' \
               test \
               | tee ./xcodebuild.log

When you have ``xcodebuild.log`` in place, run:

.. code-block:: bash

    cat xcodebuild.log | grep 'TestCase.*seconds' | awk -F '[()]' '{print $2 " -> " $1}' | sort -rn | head -5

The output you'll receive will look like this (these are the 5 slowest tests in
a suite):

.. code-block:: text

    1.957 seconds -> Test Case 'A...' passed
    0.279 seconds -> Test Case 'B...' passed
    0.274 seconds -> Test Case 'C...' passed
    0.248 seconds -> Test Case 'D...' passed
    0.201 seconds -> Test Case 'E...' passed

The trick is to use ``awk`` to capture time using regular expression ``[()]``
(left or right brace) that matches round braces in an original string produced
by ``xcodebuild`` like:

.. code-block:: text

    Test Case 'E...' passed (0.201 seconds).

``awk`` puts numbers to be the first symbols in a resulting string, skips the
braces, and that makes resulting string available for numeric sort, the rest is
self-explanatory.

I found this command particularly useful when I was looking at how to optimize
the running time of a unit test suite I was working on. I found that some of the
tests were taking 300 milliseconds to run which was unacceptable for a unit test
suite of several hundreds of tests.

Hopefully, someone will also benefit from this simple solution. Let your tests
be fast!

**Note:** Perl can also be used instead of awk:

.. code-block:: bash

    perl -ne '/(TestCase.*)\((.*)\)/ && print $2 . " -> " . $1 . "\n"' xcodebuild.log`.
