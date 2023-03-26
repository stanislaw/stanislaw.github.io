One easy way to estimate Swift vs Objective-C code ratio in iOS project
=======================================================================

:date: 2016-12-06 21:53:34
:modified: 2016-12-06 21:53:34
:tags: Swift, Objective-C
:category: Posts
:slug: 2016-12-06-one-easy-way-to-estimate-swift-vs-objc-ratio
:summary: A code snippet for estimating Swift vs Objective-C code ratio in iOS
    project.

The following finding is a result of a 5-minute brainstorm we did with `Alex
Denisov <http://lowlevelbits.org>`_. We were thinking of the fastest way to
estimate Swift vs Objective-C code ratio in an iOS application. Transitioning to
Swift can be very slow for a project which has a lot of Objective-C code, so we
want to have at least a rough understanding of how much of its code has to be
migrated from Objective-C to Swift.

We came up with a very simple heuristic: grep through the codebase and find
``@implementation`` and ``^class`` declarations for Objective-C and Swift
declarations respectively and divide Swift value by Objective-C value. Of course
this heuristic is very rough however we can make enough sense out of it in the
context of the app we are currently working on.

I have split original one-liner to be a more readable .sh script:

.. code-block:: bash

    project=./YourProject;

    objc=`grep -r "^@implementation " $project  | wc -l | tr -d ' '`;
    swift=`grep -r "^class " $project  | wc -l | tr -d ' '`;

    ratio=$(bc <<< "scale=3; $swift / $objc");
    ratio_perc=$(bc <<< "$ratio * 100");

    echo "Swift classes: $swift";
    echo "Objective-C classes: $objc";
    printf "Ratio: %0.3g%%\n" $ratio_perc;

.. code-block:: bash

    $ ./swift_vs_objc.sh
    Swift classes: 142
    Objective-C classes: 749
    Ratio: 19%

This script is very simple however I would love to have found it written by
someone else before I started looking for it a few hours ago today. So why not
keep in on this blog?
