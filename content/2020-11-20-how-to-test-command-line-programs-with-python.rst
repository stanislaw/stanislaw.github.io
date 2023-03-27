How to test command-line programs with Python tools: LIT and FileCheck
======================================================================

:date: 2020-11-20 10:00
:modified: 2020-11-20 10:00
:tags: Python
:category: Posts
:slug: 2020-11-20-how-to-test-command-line-programs-with-python
:summary: One great way of testing command-line programs with LIT and FileCheck.

In this post, I would like to share how one can test command-line programs using
a combination of LIT and FileCheck tools.

While both tools are mainly used by the LLVM compiler infrastructure developers,
they can be also used for testing any kinds of programs, not necessarily the
compiler tools.

This post is not a tutorial about using LIT/FileCheck. I will show only few
examples of what both tools can do and instead, I will focus on what are the use
cases for these tools, and in which situations both tools can be exceptionally
useful.

At the bottom of this post, I provide several helpful links about LIT/FileCheck,
some of which point to the practical step-by-step tutorials.

Where LIT/FileCheck can be used
-------------------------------

Use case 1: Testing a command-line tool with a large number of test inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have a command-line tool that you want to test against
tens/hundreds/thousands of scenarios and combinations of input arguments. LIT is
a test runner which gives you a DSL for writing your tests, something that is
more advanced than writing your custom Shell scripts.

Example of a LIT test text file:

.. code-block:: text

    RUN: command_line_program --flag1 --flag2 --flag3

LIT has a test discovery mechanism, so it is possible to specify a folder where
LIT will find all of the tests and execute them one by one or in parallel
depending on the configuration.

Use case 2: "Grep on steroids"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your command-line tool produces some output to the console, and you want to
write a test case that should match the output against a list of checks that you
define.

You would like to simply redirect the input of your program to a file and then
use ``diff`` against a pre-defined expectation file but the output of your
program contains variable lines, such as timestamps or unique identifiers, so
you cannot simply use ``diff`` because it will not understand what your program
is doing.

FileCheck is a "grep on steroids" kind of tool. You write your checks in a check
file and then run FileCheck against your program's input. FileCheck supports
several matchers, regular expressions syntax and many other features.

Example of a FileCheck check text file that matches against the output of ``git
--version`` command, e.g., ``git version 2.37.1 (Apple Git-137.1)``.

.. code-block:: text

    CHECK: git version {{\d+\.\d+\.\d+}} (Apple Git-{{.*}})

Use case 3: Test input, run commands and checks in a single file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the test maintainability perspective, it can be very convenient to contain
a whole command-line program test in one file which includes:

- Combining test runner commands, check commands, and test input in one file

. An example is better than a long explanation. Let's assume we want to test
that our C program, when compiled and run, produces a given output. Here's how a
FileCheck/LIT test could look like:

.. code-block:: text

    // RUN: clang -o hello_program %s
    // RUN: ./hello_program | filecheck %s
    // CHECK: Hello world!

    #include <stdio.h>

    int main() {
      printf("Hello world!\n");
      return 0;
    }

This file is a C program and a LIT/FileCheck test at the same time:

- The C compiler ignores the // comments.
- The LIT/FileCheck are only interested in RUN/CHECK statements.

The RUN statements are run by LIT which interprets the ``%s`` as "this file".
The RUN statements do the following:

- Run the ``clang`` command
- Execute the compiled ``hello_program`` program whose output is connected to
  the input of ``filecheck``.

FileCheck receives the output from the ``hello_program`` and matches it against
its only ``CHECK:`` which is ``Hello world!``.

.. code-block:: text

    lit .
    -- Testing: 1 tests, 1 workers --
    PASS: <unnamed> :: hello.test.c (1 of 1)

    Testing Time: 0.50s
      Passed: 1

The rest of this post explains in more detail what are LIT and FileCheck.

What is LIT?
------------

LLVM LIT is a testing tool developed for `LLVM <https://llvm.org/>`_, a
collection of modular and reusable compiler and toolchain technologies. LIT
stands for LLVM Integrated Tester and was created to provide a flexible and
lightweight testing framework for LLVM.

LIT is a flexible and extensible test runner program. It can run any kinds of
command-line programs, without any limitations or requirements of connection to
the LLVM ecosystem.

LIT works with text files, and it executes commands that are prefixed with
``RUN:`` keyword. Each command is run by LIT in a sub-shell process.

.. code-block:: bash

    RUN: command_line_program --some-flag1
    RUN: command_line_program --some-flag2
    RUN: command_line_program --some-flag3

When LIT runs such a test, each ``RUN``-command must exit with ``0``, otherwise
the test will fail.

LIT can be configured to work with files of any extension but let's say, the
above test file is called ``test.itest``.

When LIT is minimally configured (see `Tutorial: LIT and FileCheck
<https://filecheck.readthedocs.io/en/stable/04-tutorial-lit-and-filecheck.html>`_
for more details), the following command will run the above test:

.. code-block:: bash

    lit test.itest

The output produced by LIT should be as follows:

.. code-block:: text

    lit test.itest

    -- Testing: 1 tests, single process --
    PASS: <unnamed> :: test.itest (1 of 1)
    Testing Time: 0.10s
      Expected Passes    : 1

An example of a LIT test that will always fail:

.. code-block:: bash

    RUN: false

A typical failed test output:

.. code-block:: text

    lit -v test.itest
    -- Testing: 1 tests, 1 workers --
    FAIL: <unnamed> :: test.itest (1 of 1)
    ******************** TEST '<unnamed> :: test.itest' FAILED ********************
    Script:
    --
    : 'RUN: at line 1';   false
    --
    Exit Code: 1

    ********************
    ********************
    Failed Tests (1):
      <unnamed> :: test.itest

    Testing Time: 0.17s
      Failed: 1

What is LLVM FileCheck?
-----------------------

LLVM FileCheck is an utility tool that is part of the LLVM project. It is used
for checking the contents of files against expected patterns or contents, and it
is often used for testing LLVM components and tools.

FileCheck works by reading a file and searching for patterns that match certain
regular expressions. It can be configured to check for the presence or absence
of specific strings or patterns, and it can be used to check for specific
numbers, variables, or other types of data.

Let's consider a LIT test that uses ``filecheck`` to assert that a program
produces expected output.

.. code-block:: bash

    RUN: command_line_program --say-hello-world | filecheck %s
    CHECK: Hello World

``filecheck`` acts as a more advanced version of ``grep``. It consumes the
output of the ``command_line_program`` via stdin and reads the ``CHECK:`` checks
from a file that is specified as ``%s`` input argument. The ``%s`` is translated
to "a full path to this file" by LIT, see `lit - LLVM Integrated Tester -
Substitutions <https://llvm.org/docs/CommandGuide/lit.html#substitutions>`_.

Under the hood, ``filecheck`` reads the test file and finds all the CHECK:
statements. ``filecheck`` enumerates over a list of checks and for every input
line received via stdin, ``filecheck`` tries to match the input line with a
current ``CHECK`` statement. If a ``CHECK`` statement can be matched, this check
is removed from the list of checks, and the enumeration continues further.

If all ``CHECK`` statements could be matched with the lines from the ``stdin``
input, ``filecheck`` exits with ``0`` producing no output to the console.
Otherwise, it exists with non-zero code and reports an error.

Here's an example of how a LIT test can fail because of a failed check by
FileCheck:

.. code-block:: bash

    -- Testing: 1 tests, single process --
    FAIL: <unnamed> :: test.itest (1 of 1)
    ******************** TEST '<unnamed> :: 02-fail.c' FAILED ********************
    test.itest:2:8: error: CHECK: expected string not found in input
    CHECK: Hello World
           ^
    <stdin>:1:1: note: scanning from here
    Something else
    ...
    ********************
    Testing Time: 0.11s
    ********************
    Failing Tests (1):
        <unnamed> :: test.itest

      Unexpected Failures: 1

Real-world LIT/FileCheck test suites
------------------------------------

Here are some examples of the LIT/FileCheck test suites found on GitHub:

- `LLVM's integration tests
  <https://github.com/llvm/llvm-project/tree/main/llvm/test>`_
- `WebAssembly/binaryen
  <https://github.com/WebAssembly/binaryen/tree/main/test/lit>`_
- `Mull, mutation testing system
  <https://github.com/mull-project/mull/tree/main/tests-lit>`_
- `StrictDoc, documentation tool
  <https://github.com/strictdoc-project/strictdoc/tree/main/tests/integration>`_

Conclusion
----------

LIT can serve as a perfect replacement for a bunch of hand-crafted Shell
scripts. The simple DSL of ``RUN:`` commands and LIT's Substitutions such as
``%s`` help to organize the test commands.

FileCheck serves as "grep on steroids" kind of tool. It helps to match tested
program output against user-defined checks stored in a text file.

As explained above in `Use case 3: Test input, run commands and checks in a
single file`_, the option of combining LIT/FileCheck's RUN/CHECK statements with
test inputs increases the maintainability of the test suites.

LIT/FileCheck documentation
---------------------------

- `LLVM documentation - lit - LLVM Integrated Tester
  <https://llvm.org/docs/CommandGuide/lit.html>`_
- `LLVM documentation - FileCheck - Flexible pattern matching file verifier
  <https://llvm.org/docs/CommandGuide/FileCheck.html>`_
- `LLVM Testing Infrastructure Guide <https://llvm.org/docs/TestingGuide.html>`_
- `Tutorial: LIT and FileCheck
  <https://filecheck.readthedocs.io/en/stable/04-tutorial-lit-and-filecheck.html>`_
- `Using LLVM LIT Out-Of-Tree
  <https://medium.com/@mshockwave/using-llvm-lit-out-of-tree-5cddada85a78>`_
- `FileCheck.py, A Python port of LLVM FileCheck
  <https://github.com/mull-project/FileCheck.py>`_
