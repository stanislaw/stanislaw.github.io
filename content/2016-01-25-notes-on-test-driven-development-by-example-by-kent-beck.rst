Notes on "Test-Driven Development by Example" by Kent Beck
==========================================================

:date: 2016-01-25 09:40:04
:modified: 2016-01-25 09:40:04
:tags: Testing, TDD, Books
:category: Posts
:slug: 2016-01-25-notes-on-test-driven-development-by-example-by-kent-beck
:summary: This is my notes on "Test-Driven Development by Example", book by Kent
    Beck published in 2004.

During the past year I have read quite a few books and some of them were related
exclusively to the TDD topic, especially "Growing Object-Oriented Software
guided by Tests" by Steve Freeman and Nat Pryce. After having that book read, I
felt that my understanding of TDD was much better than it had been before, so I
was going to read something else but then I watched a talk by Steve Freeman
where he recommends reading "Test-Driven Development by Example" and also then
recommends re-reading it every 1 or 2 years, so valuable and deep this book is.

So I decided to follow Steve's advice and did read the book very thoroughly. Now
I see how two books complement each other, so that it is hard to say where I
learned what about TDD from, anyway the following is the summary of what makes
Kent's book special for my understanding and practice of TDD.

Clean code that works
---------------------

    "Clean code that works (Ron Jeffries)" - is the goal of Test-Driven
    Development. (preface, p.ix)

Two rules of TDD
----------------

- Write new code only if an automated test has failed
- Eliminate duplication (preface, p.ix)

TDD cycle
---------

The two rules imply an order to the tasks of programming.

    1. Red - Write a little test that doesn't work, and perhaps doesn't even
       compile at first.
    2. Green - Make the test work quickly, committing whatever sins necessary in
       process.
    3. Refactor - Eliminate all of the duplication created in merely getting the
       test to work.

    Red/green/refactor – the TDD mantra. (preface, p.x)

In other chapter the same order is described as "general TDD cycle":

    The general TDD cycle goes as follows.

    1. Write a test...
    2. Make it run...
    3. Make it right...

    The goal is clean code that works (thanks to Ron Jeffries for this pithy
    summary)... First we'll solve the "that works" part of the problem. Then
    we'll solve the "clean code" part. This is the opposite of
    architecture-driven development, where you solve "clean code" first, then
    scramble around trying to integrate into the design the things you learn as
    you solve the "that works" problem. (p.11)

There is also a bit more detailed version which is called a "rhythm of TDD":

    - Quickly add test
    - Run all tests and see the new one fail
    - Make a little change
    - Run all tests and see them all succeed
    - Refactor to remove duplication (p.1)

Write a failing automated test before you write any code
--------------------------------------------------------

This quote appears to be a very famous one:

    I taught Bethany, my oldest daughter, TDD as her first programming style
    when she was about age 12. She thinks you can't type in code unless there is
    a broken test. The rest of us have to muddle through reminding ourselves to
    write the tests.

I am the one who have been teaching himself to write tests and then write tests
upfront during past 4 or 5 years however I still have to remind myself to follow
this first rule of TDD. In iOS development it is sometimes tempting to skip
"test first" part when you have to implement some UI feature on top of
half-tested UI code: when I think about writing failing test for that new
feature I know that I have to do quite a lot of exercises against iOS testing
infrastructure (which is far from being mature yet) to make that UI test case to
reflect my new feature and fail adequately and that makes me to procrastinate
about writing that test first.

Somewhere in the middle of the book and at the same time while I was working on
bunch of UI features of that kind I saw a dream where I was listening to a
lecture by some university professor who was talking about importance of writing
failing test first even in complex cases such as legacy UI code or lack of
proper testing tool and infrastructure support. I don't remember anything else
from that dream anymore but memory of it now serves me very well as additional
personal reminder of virtue of always following the first rule of TDD.

Three techniques for quickly getting to green
---------------------------------------------

- Fake It
- Obvious Implementation
- Triangulation

Fake It
~~~~~~~

    Return a constant and gradually replace constants with variables until you
    have the real code. (p.13)

Obvious implementation
~~~~~~~~~~~~~~~~~~~~~~

    Type in the real implementation.

    When I use TDD in practice, I commonly shift between these two modes of
    implementation. When everything is going smoothly and I know what to type, I
    put in Obvious Implementation after Obvious Implementation (running the
    tests each time to ensure that what's obvious to me is still obvious to the
    computer). As soon as I get unexpected red bar, I back up, shift to faking
    implementations, and refactor to the right code. When my confidence returns,
    I go back to Obvious Implementations. (p.13)

    How do you implement simple operations? Just implement them.

    Fake It and Triangulation are teensy-weensy tiny steps. Sometimes you are
    sure you know how to implement an operation. Go ahead. For example, would I
    really use Fake It to implement something as simple as plus()? Not usually.
    I would just type in the Obvious Implementation. If I noticed I was getting
    surprised by red bars, then I would go to smaller steps... (p.154)

    ...There's no particular virtue in the halfway nature of Fake It and
    Triangulation. If you know what to type, and you can do it quickly, then do
    it. (p.154)

Triangulation
~~~~~~~~~~~~~

    How do you most conservatively drive abstraction with tests? Abstract only
    when you have two or more examples. (p.153)

    If two receiving stations at a known distance from teach other can both
    measure the direction of a radio signal, then there is enough information to
    calculate the range and bearing of the signal. This calculation is called
    Triangulation.

    By analogy when we triangulate, we only generalize code when we have two
    examples or more... When the second example demands a more general solution,
    then and only then do we generalize (p.16).

    I only use Triangulation when I'm really, really unsure about the correct
    abstraction for the calculation. Otherwise I rely on either Obvious
    Implementation or Fake It. (p.154)

Moving at different speeds
--------------------------

    You want to maintain that red/green/refactor rhythm. Obvious Implementation
    is second gear. Be prepared to downshift if your brain starts writing checks
    your fingers can't cash. (p.155)

    If you don't know what to type, type the Obvious Implementation. If you
    don't know what to type, then Fake It. If the right design still isn't
    clear, then Triangulate. If you still don't know what to type, then you can
    take that shower. (p.138)

Duplication
-----------

"Removing duplication as a way to drive design" - this is one of the key topics
in the book but I am still not sure if that is (or should be) the only way to
drive design. Though definitely removing duplication is very strong source of
design changes. I'll make sure to keep an eye on this idea.

Test is an Object
-----------------

Very interesting side-effect Kent's book produced was that I finally noticed and
recognized incorrectness of semantics that is suggested by default Xcode
templates and that I have been following blindly all those years.

When you create fresh Xcode project with "Include Unit Tests" mark enabled you
end up with dummy unit test class generated automatically by Xcode:

.. code-block:: swift

    class TriangleTests: XCTestCase {
        func testExample()
    }

There is one very bad semantic error that happens here: the class name for test
case generated for project Triangle is in plural: **TriangleTests**: if my name
of my test class has "Tests" postfix then I no longer treat it as an object,
i.e. small machine that performs testing according to its well-defined scope,
instead I have umbrella or bag with a bunch of tests most likely without a good
cohesion between them.

Some years ago when I switched from Ruby on Rails with RSpec as BDD-style
testing framework that I mostly used to iOS development and Xcode with their
default xUnit-style: OCUnit and then XCTest – I couldn't get how to live without
nested ``describe`` blocks inside those ``MyTests: XCTestCase`` classes. Now
having deeper insight into difference between two approaches: xUnit style and
BDD style I now prefer xUnit style. What ``describe`` is in Cedar/Kiwi becomes
one class in xUnit given that most often I can flatten too nested structure of
my tests. This insight has very positive effect on how I organize integration
and especially functional tests (test for UI components and groups of them taken
in isolation from the whole iOS application as I have described in `Test
Automation for iOS
</2015-12-14-test-automation-for-ios-written-for-blacklane-tech-blog.html>`_.

In my example this test class should have singular name: ``TriangleTest``. If
there will be a large number aspects we can start creating classes one for each
aspect: ``TriangleAspectTest`` or ``Triangle_Aspect_Test``. That's what I
started doing on daily basis with functional tests: good example is mobile app's
screen with number of different success / failure user paths - in this case test
class corresponds to one aspect of a feature that screen represents.

This topic is not covered in this book but still I have found indirect examples
of Kent's reasoning about fixtures which makes me think I am on the right track:

    "In general if I find myself wanting a slightly different fixture then I
    start new subclass of Test Case." (p.160)

    "All of the tests that share a single fixture will be methods in the same
    class. Test that requires a different fixture will be in a different class."
    (p.162)

Below see also "Self Shunt": this technique makes sense only if classes have
focus i.e. they are not the "lists of tests" but something more object- or
better subject-oriented.

Self Shunt
----------

    How do you test that one object communicates correctly with another? Have
    the object under test communicate with the test case instead of with the
    object it expects.

    ...Why do we need a separate object for the listener? We can just use the
    test case itself. The TestCase itself becomes a kind of Mock Object (p.145)

Broken Test and Clean Check-in
------------------------------

Broken Test is for solo programming:

    How do you leave a programming session when you're programming alone? Leave
    the last test broken... When you come back to the code, you then have an
    obvious place to start. (p.149)

Clean Check-in is for team programming:

    How do you lave a programming session when you're programming in a team?
    Leave all of the tests running.

How much feedback do you need?
------------------------------

Kent gives an example:

    Given three integers representing the length of the sides of a triangle,
    return:

    1. if the triangle is equilateral
    2. if the triangle is isosceles
    3. if the triangle is scalene

    and throw an exception if the triangle is not well formed.

He shows his implementation and 6 tests he wrote for this problem. He says that
some tester wrote 65 tests for the same problem.

I have `tried mine <https://gist.github.com/stanislaw/9407f178a525a2cc4901>`_
using Swift and I got 11 tests given I wanted to test incorrect input for all 3
sides: negative and zero-cases.

To summarize:

    TDD's view of testing is pragmatic. In TDD, the tests are means to an
    end–the end being code in which we have great confidence. If our knowledge
    of implementation gives us confidence even without test, then we will not
    write that test. Black box testing, where we deliberately choose to ignore
    the implementation, has some advantages. By ignoring the code, it
    demonstrates a different value system - the tests are valuable alone. It's
    an appropriate attitude to take in some circumstances but that is different
    from TDD. (p.197)

xUnit
-----

    There are two reasons for implementing xUnit yourself, even if there is a
    version already available:

    - Mastery - The spirit of xUnit is simplicity. Martin Fowler said, "Never in
      the annals of software engineering was so much owned by so many to so few
      lines of code"... Rolling your own will give you a tool over which you
      have a feeling of mastery.
    - Exploration - When I'm faced with a new programming language, I implement
      xUnit. By the time I have the first eight to ten tests running, I have
      explored many of the facilities I will be using in daily programming.

Influence diagrams
------------------

Kent uses influence diagrams inspired by Gerry Weinberg's Quality Software
Management:

The "no time for testing" death spiral
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    An arrow between nodes means that an increase in the first node implies an
    increase in the second node. An arrow with a circle means that an increase
    in the first node implies a decrease in the second node. What happens when
    the stress level rises?

    The "no time for testing" death spiral:

.. figure:: {static}/images/2016-01-25-notes-on-test-driven-development-by-example-by-kent-beck/Figure-25.1.JPG
    :alt: Figure 25.1 "No time for testing" death spiral

    **Figure 25.1 "No time for testing" death spiral**

----

    This is a positive feedback loop. The more stress you feel, the less testing
    you will do. The less testing you do, the more errors you will make. The
    more errors you make, the more streess you feel. Rinse and repeat.

    How do you get out of such a loop? Either introduce a new element, replace
    one of the elements, or change the arrows. In this case we'll replace
    Testing with Automated Testing.

    Did I just break something else with that change?" Figure 25.1 shows the
    dynamic at work. With automated tests, when I start to feel stress, I run
    the tests. Tests are the Programmer's Stone, transmuting fear into boredom.
    "No, I didn't break anything. The tests are all still green." The more
    stress I feel, the more I run the tests. Running the tests immediately gives
    me a good feeling and reduces the number of errors I make, which further
    reduces the stress I feel."

    "We don't have time to run the tests. Just release it!" The second picture
    isn't guaranteed. If the stress level rises high enough, it breaks down.
    However, with the automated tests you have a chance to choose your level of
    fear. (p.124)

Not enough time to test reduces the available time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: {static}/images/2016-01-25-notes-on-test-driven-development-by-example-by-kent-beck/Figure-A.5.JPG
    :alt: Figure A.5 Not enough time to test reduces the available time

    **Figure A.5 Not enough time to test reduces the available time**

----

    When you have a system that isn't behaving, you do have options.

    - Drive a positive feedback loop the other direction. If you have a loop
      between tests and confidence, and tests have been failing thus reducing
      confidence, then you can make more tests work to increase confidence in
      your ability to get more tests working.
    - Introduce a negative feedback loop to control an activity that has grown
      too large.
    - Create or break connections to eliminate loops that are not helping.
      (p.210)

When should you delete tests?
-----------------------------

    More tests are better, but if two tests are redundant with respect to each
    other, should you keep them both around? That depends on two criteria.

    - The first criterion for your tests is confidence. Never delete a test if
      it reduces your confidence in the behavior of the system.
    - The second criterion is communication. If you have two tessts that
      exercise the same path through the code, but they speak to different
      scenarios for a reader, leave them alone.

    That said, if you have two tests that are redundant with respect to
    confidence and communication, delete the least useful of the two.

Fear vs Confidence
------------------

    Tests are programmer's Stone transforming fear into boredom...

And another variation:

    Write tests until fear is transformed into boredom...

Lesson learned: move slowly
---------------------------

    @sbpankevich: Reading TDDbE and hear Kent's voice in my head: start with
    failing test, move slowly. Now I move as slowly as never did. Thanks
    @KentBeck !

    @KentBeck: @sbpankevich the trick is to move slowly very very frequently

taken from https://twitter.com/KentBeck/status/685494067120099328.

Lesson learned: don't stay red longer than 1 minute
---------------------------------------------------

This is the rule that I introduced for myself while reading this book. I started
following it and it helped me to be more careful and conscious when I was doing
some refactorings of critical parts of code at my work. Given infrastructure
details of UI testing or Functional Testing in iOS, "1 minute" for me resorts to
smallest possible step that I can make when starting from green state.

Conclusion
----------

By taking and then publishing these notes I wanted to achieve two goals:

- Internalize better the knowledge that I got from reading this great book of
  Kent Beck.
- Expose some of ideas and insights that I found interesting in this book to
  inspire others to read it as well.

I have definitely managed to accomplish the first of the above goals but am not
sure if I did succeed in the second: from my experience, notes like these can at
best expose no more than 10% of the overall information from subject, so if
you're reading this and still didn't read this book, make sure to read it - for
me it is one of the best on my book shelf.
