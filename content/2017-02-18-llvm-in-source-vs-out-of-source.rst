LLVM-based project and CMake: choosing between in-source and out-of-source hosting
==================================================================================

:date: 2017-02-18 20:05:00
:modified: 2017-05-05 19:20:00
:tags: LLVM, CMake
:category: Posts
:slug: 2017-02-18-llvm-in-source-vs-out-of-source
:summary: LLVM-based project and CMake: in-source vs out-of-source hosting.

**Disclaimer:** the following summary is based on our limited experience with
`Mull project <https://github.com/mull-project>`_ and some other smaller
research projects and is only applicable to the projects that can live outside
of LLVM source tree. If you intend your project to become a part of LLVM source
tree you obviously have no choice other than hosting your project in-source.

TL;DR
-----

.. raw:: html

    <style>
    table {
      border:none;
      border-collapse: collapse;
      border-spacing: 0px;
      table-layout : fixed;
    }

    table td {
      border: 1px solid #ddd;
      margin: 0px;
      padding: 4px;
    }

    table th {
      margin: 0px;
      padding: 4px;
    }

    table td:first-child { border-left: none; }
    td:first-child + td { text-align: center; }
    td:first-child + td + td { text-align: center; }

    table tr:nth-child(even) {
        background-color: #eee;
    }
    table tr:nth-child(odd) {
        background-color: #fff;
    }
    table th {
        color: white;
        background-color: gray;
    }

    .green {
      color: #009966;
      font-weight: bold;
    }

    </style>

    <table style="width: 100%;">
      <tr>
        <th>Criteria</th>
        <th>In-source</th>
        <th>Out-of-source</th>
      </tr>
      <tr>
        <td>Access to LLVM source code</td>
        <td><span class="green">Full access</span></td>
        <td>Limited access</td>
      </tr>
      <tr>
        <td>CMake generation</td>
        <td>Slower</td>
        <td>Faster</td>
      </tr>
      <tr>
        <td>Project structure, navigation</td>
        <td>Your code and LLVM code</td>
        <td>Only your code</td>
      </tr>
      <tr>
        <td>First build time</td>
        <td>Slow</td>
        <td><span class="green">Very fast</span></td>
      </tr>
      <tr>
        <td>Indexing</td>
        <td>Slow</td>
        <td><span class="green">Much faster</span></td>
      </tr>
      <tr>
        <td>CMake API</td>
        <td>CMake API, LLVM CMake API</td>
        <td>CMake API</td>
      </tr>
      <tr>
        <td>Project dependencies</td>
        <td>Might be implicit</td>
        <td>Explicit</td>
      </tr>
      <tr>
        <td>Continuous Integration</td>
        <td>Might be slower</td>
        <td><span class="green">Much faster</span></td>
      </tr>
      <tr>
        <td>Distribution</td>
        <td>Might be harder</td>
        <td>Might be easier.</td>
      </tr>
    </table>

For the scope of this post, these are the simple explanations of in-source and
out-of-source kinds of hosting.

**In-source:**

- You clone LLVM sources.
- In LLVM source code there are specific folders provided where you can embed
  your project so that you can develop your project inside of LLVM source code.
- You run CMake which generates a project structure which includes both your
  project's code and LLVM.
- **When you build project you also build LLVM source code that your project
  depends on.**

The greatest example of an in-source project is Clang. This article demonstrates
it very well how to build Clang inside of the LLVM source tree: `Getting Started
With LLVM/Clang on OS X
<https://lowlevelbits.org/getting-started-with-llvm/clang-on-os-x/>`_ (by the
way, this was my very first tutorial I followed to get started with LLVM).

**Out-of-source:**

- You have only your project's source code based on CMake.
- You configure your CMake to link against LLVM's libraries already prebuilt by
  you or someone else before (the easiest way to obtain LLVM binaries on Mac OS
  is to just type: ``brew install llvm`` and find them in
  ``/usr/local/opt/llvm``).
- **You don't build LLVM source code but only link with LLVM libraries that you
  or someone else have built already outside of your source tree.**

Access to LLVM source code
--------------------------

With in-source hosting you have a full access to LLVM source code. This might be
useful if you have to explore LLVM source code and required if you want to
change LLVM source code itself.

With out-of-source hosting you only have access to a public API of LLVM code, it
is not easy to debug and is not possible to change LLVM internals.

This is the major and probably the only advantage of an in-source way of hosting
over its out-of-source counterpart.

CMake generation
----------------

CMake generation is what happens when you run ``cmake`` with your favorite
generator like Xcode, Ninja or Make to create a ``Build`` folder with your
project.

The difference in generation time for in-source and out-of-source project is not
significant but is still very noticeable especially if you happen to change a
layout of your CMakeLists files often.

Project structure and navigation
--------------------------------

With in-source hosting your project's structure carries your code and the code
from the whole LLVM source tree. It is likely that your project uses only a
subset of LLVM API so you will have a lot of code that you will never use.

In Xcode CMake generator doesn't populate schemes by default so that you can
select them manually, however all of the build targets and their folders are
there and that makes a navigation harder (``LLVM.xcodeproj`` of LLVM 3.9 has
something around 170 targets).

With out-of-source hosting a project structure is entirely yours: only your
source code and a few targets of your project.

First build time
----------------

The difference in build time is the most significant. With in-source, if your
project has 50 files you additionally build a few hundreds of LLVM source files
(Mull dependencies make up to 800 of LLVM files). With out-of-source, you only
build your 50 files and then link a number of pre-built LLVM libraries.

With a newly-generated in-source Xcode project it is also harder to switch
between DEBUG/RELEASE configurations. You use DEBUG when you develop, but then
you want to test your project in RELEASE configuration and that makes you wait
another round of RELEASE compilation which takes even more time because of
optimizations.

Indexing
--------

After you open your CMake-generated project Xcode needs to index your project so
that it can do a number of things for you, to name a few:

- syntax highlighting
- auto-completion
- interactive code analysis
- "jump to definition" (Command + click)
- "open quickly" (Command + Alt + O).

For Xcode it takes longer to index an in-source project (remember: it is 50
files of your project and ~3500 files of LLVM). It is not clear whether Xcode is
smart enough to index only the targets that you actually use however even with
that the difference in speed is very noticeable.

CMake API
---------

With an in-source approach, an integration with LLVM CMake macros is another
level of complexity you have to maintain on top of native CMake API. For
newcomers who are new to LLVM/CMake this might extend their learning curve as
instead of learning just CMake docs they have to also learn the
``llvm/cmake/modules/*`` scripts.

With an out-of-source hosting you have a direct access to CMake API without any
overhead of LLVM's CMake infrastructure. Of course the maintainers of LLVM CMake
API evolved their scripts to address a number of issues on various platforms so
you will still have to learn from their experience.

Dependencies
------------

With an in-source project, when you use LLVM CMake scripts, they do a number of
good things for you, but this comes at cost of additional magic that is
sometimes hard to see. Switch of your project from in-source to out-of-source
might reveal these issues like missing ``@rpath`` settings or missing linkage to
``zlib`` and ``ncurses``. ``llvm-config`` tool is very useful if you want to
learn about what actually LLVM's dependencies are.

Continuous Integration
----------------------

With in-source project, CI process that includes building LLVM code cannot be
anything but slower: cloning LLVM sources and building them takes time.

Of course, if your project gets into LLVM source tree, you will get CI "out of
the box" because LLVM CI setup is maintained by LLVM community and so is very
well-engineered.

With out-of-source tree project a CI build process will probably be must faster,
something like:

- ``brew install llvm@x.x`` (just fetching the binaries to a build machine, no
  clone, no build)
- clone and build your project with CMake
- run tests

Distribution
------------

Whatever distribution type you plan for your project it will probably be
dependent on the criteria described above: build times, continuous integration
and dependencies.

With an out-of-source tree project, its distribution might be a bit easier: its
LLVM dependencies are already outside and that makes this setup closer to what
the users will have to deal with in the wild.

Summary
-------

Our conclusion is that the only real advantage an in-source hosting has over its
out-of-source counterpart is the full access to LLVM source code while the main
advantage of out-of-source hosting is a much faster build process.

When you develop inside LLVM source tree, you project "is LLVM" in a way. When
you develop it outside, you are "a client of LLVM", of its public API.

One reason why a developer might have to choose in-source hosting for a project
can be that this project requires changes of LLVM source code for the project to
work. Author of `Mull <https://github.com/mull-project>`_ project originally
started it as in-source project because he expected problems with running the
code of test suites based on GoogleTest via LLVM ORC JIT, however with time it
became clear that Mull worked perfectly against stable versions of LLVM API
without any modifications so now we are now transforming Mull into an
out-of-source project.

One open question that we still have is how to combine the advantages of both
approaches in the same source tree. It is not clear how to make two parallel
CMake hierarchies: custom one and LLVM-based to co-exist together. We are going
to clarify this with time.

I will be happy to learn about your experience with in-source vs out-of-source
tree projects, feel free to `drop me a line <mailto:s.pankevich@gmail.com>`_.
