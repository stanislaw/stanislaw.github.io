---
layout: post
title: "XCTest: focused tests"
date: 2017-02-15 11:05:00 +0200
keywords: "Swift, Objective-C, XCTest, testing"
description: "Programmatic approach to running XCTests in a focused mode."
---

Ability to run only one test or tests from one test case class is a feature
I have been missing for years in Xcode, in SenTestingKit and then XCTest
frameworks.

Yes, it is possible to run only one test by clicking on a small icon next to a
test method's name or using keyboard combination:
`Control + Option + Command + U` however both of these methods are:

1) still very unstable in Xcode up until current 8.2.1. They stop working after
you do a number of iterations on a test file, especially change the test method
names, remove or add them. Highlighting is lost, icons disappear, key
combination no longer works.

2) developer-unfriendly: so far I have never seen a developer who would be doing
real TDD using mouse. Yes, we have to click on those icons and also put a cursor
on a test body to make `Control + Option + Command + U` work but that's not an
IDE experience I would like to have.

Ruby testing frameworks support programmatic focused tests feature for ages,
Mocha supports it, Cedar supports it. Why don't we have such a feature in
XCTest.

Recently I looked into XCTest framework's headers and found that Apple had
exposed some of the very useful classes. Using these classes a developer can
build his own custom test suite and run it programmatically outside of a
context of Unit Testing Bundle target where XCTests are not under programmer's
control.

The following is a proof of concept that seems to work. I haven't tested it on
large test suites but I don't see any reasons why it would not work
at scale.

### Test runner

`XCTestSuite.default()` gives us all tests that are run by default. Tests are
grouped into XCTestSuite classes. We enumerate through them recursively and look
for focused tests.

Simple rule is used: methods with `_focus_` in their names and classes with
`Focus` in their names are included to a focused test suite.

<pre>
let defaultSuite = XCTestSuite.default()

let focusedTestSuite = XCTestSuite(name: "Focused Test Suite")

var testSuites = [defaultSuite]
while let testSuite = testSuites.popLast() {
  for testOrSuite in testSuite.tests {
    if let test = testOrSuite as? XCTestCase {
      /// Test should have `_focus` to be included to the focused test suite.
      if let testName = test.name, testName.contains("_focus_") {
        focusedTestSuite.addTest(test)
      }
    }

    else if let testSuite = testOrSuite as? XCTestSuite {
      /// Test class should have `Focus` in its name to be included to the
      /// focused test suite.
      if let testSuiteName = testSuite.name, testSuiteName.contains("Focus") {
        focusedTestSuite.addTest(testSuite)
      } else {
        testSuites.append(testSuite)
      }
    }

    else {
      assert(false, "Should not reach here. If it does, we learn!")
    }
  }
}

if focusedTestSuite.tests.count > 0 {
  print("Focused tests were detected: running them in a custom test suite.")
  focusedTestSuite.run()
} else {
  print("No focused tests. Running default test suite.")
  defaultSuite.run()
}
</pre>

### Test observer

Test observer is needed to track a progress of a test suite run. Here we are
only interested in seeing if there are any failing tests. If they are we
probably want to exit with a non-zero exit code which is relevant for
integration to a build process.

<pre>
class TestObserver: NSObject, XCTestObservation {
  var testsFailed = 0
}

let testObserver = TestObserver()

let observationCenter = XCTestObservationCenter.shared()
observationCenter.addTestObserver(testObserver)

<... Runner code ...>

if focusedTestSuite.tests.count > 0 {
  print("Focused tests were detected: running them in a custom test suite.")
  focusedTestSuite.run()
} else {
  print("No focused tests. Running default test suite.")
  defaultSuite.run()
}

if (testObserver.testsFailed > 0) {
  return 1
}

return 0;
</pre>

### Summary

The proof of concept seems to be working. Obviously it should also be
straightforward to add a `skip` feature: skipping test methods or the whole
test classes so that they are not executed by a test runner.

Check out the full source code [here](https://github.com/stanislaw/Examples/tree/20170213-focused-xctest).

Also explore the headers of XCTest framework. They can be found
in `/Applications/Xcode.app//Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks/` directory.
