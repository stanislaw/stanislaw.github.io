Reentrant parser using Flex and Bison
=====================================

:date: 2016-03-29 02:04:34
:modified: 2016-03-29 02:04:34
:tags: Flex/Bison, Parsing
:category: Posts
:slug: 2016-03-29-reentrant-parser-using-flex-and-bison
:summary: Reentrant aka thread-safe parser based on Flex and Bison and
    integrated to Xcode project (Mac OS X).

Introduction
------------

In this post I share my knowledge I gained around the process of creation of
reentrant aka thread-safe parser based on Flex and Bison and integrated to Xcode
project (Mac OS X).

The post consists of two parts:

1. quick introduction to Flex and Bison with example
2. example of reentrant parser implemented and integrated to Xcode project.

Feel free to skip introduction and proceed to section `Reentrant parser
<#Reentrant-parser>`_ or even jump straight to `example project on Github
<https://github.com/stanislaw/Examples/tree/20160328-reentrant-parser-with-flex-and-bison>`_
if you know exactly what you are looking for.

This post is complemented by another post: `Flex and Bison: tips for beginners
</2016-04-02-flex-and-bison-tips-for-beginners.html>`_ where I collect tips that
I think might be useful for folks who only start learning Flex and Bison.

What are Flex and Bison?
------------------------

For complete definitions, you may read these projects pages: `Flex
<http://flex.sourceforge.net/>`_ and `Bison
<https://www.gnu.org/software/bison/>`_. For this post, the following simplified
explanation will suffice:

Flex is a program that generates "lexer" (also called "scanner" or "tokenizer")
based on grammar you specify in a special format. Given some input this
generated lexer recognizes tokens (also called lexical patterns) and for each
token recognized executes specific C code corresponding to that token.

Flex can be used as standalone tool but most often it is used together with
Bison: Flex delegates execution of "specific C code" corresponding to particular
token to Bison, so that responsibility of Lexer is to produce tokens and
responsibility of Bison is to decide what to do with those tokens, what actions
to do.

In a nutshell, imperatively, parser is a switch-of-switches-...of-switches. Flex
and Bison provide developers with a higher-level abstraction to write their
parsers in a declarative way while those tools generate imperative parsing
machinery in C language under the hood.

Note: in context of Flex/Bison there are two meanings of the word "parser" and
both of them are used very often: parser as Bison (compared to Flex as lexer)
and parser as the Flex+Bison together (which is actually lexer + parser).

Use case examples
~~~~~~~~~~~~~~~~~

Flex/Bison can be useful for parsing of anything that has grammar, explicit or
implicit. Non-exhaustive list includes:

- Compilers
- Parsers
- Domain-Specific Languages
- Validators / lint tools

One example where I first saw Flex and Bison in action was `toy assembler
compiler <https://github.com/AlexDenisov/Hasm>`_. Here are examples: of its
`Flex grammar
<https://github.com/AlexDenisov/Hasm/blob/c90bdd2ff72523e40b143f3379e7a264d8a18760/Hasm/Tokenizer/Lexer.lm>`_
and `Bison grammar
<https://github.com/AlexDenisov/Hasm/blob/c90bdd2ff72523e40b143f3379e7a264d8a18760/Hasm/Parser/Parser.ym>`_.

My own use case is parser of terminal input that I am writing as part of my toy
terminal. Writing terminal includes dealing with numerous `escape sequences
<http://invisible-island.net/xterm/ctlseqs/ctlseqs.html>`_ so I use Flex and
Bison to deal with those details on a higher level.

Simple example
~~~~~~~~~~~~~~

Original of this simplified example is demo project I have created: `Reentrant
parser with Flex and Bison
<https://github.com/stanislaw/Examples/tree/20160328-reentrant-parser-with-flex-and-bison>`_.

Here is fragment of its Flex's grammar where lexer recognizes numbers and
strings from input it is given:

.. code-block:: text

    NUMBER [0-9]+
    STRING [A-Z]+
    SPACE \x20

    {NUMBER} {
        yylval->numericValue = (int)strtoul(yytext, NULL, 10);

        printf("[Lexer, number] %s\n", yytext);

        return Token_Number;
    }

    {STRING} {
        yylval->stringValue = strdup(yytext);

        printf("[Lexer, string] %s\n", yytext);

        return Token_String;
    }

    {SPACE} {
        // Do nothing, just eat spaces
    }

By setting ``yylval->...`` and returning specific Token Flex notifies Bison that
it should take some action on it. If Flex receives space character it just
ignores it without letting parser about it.

Corresponding Parser's grammar:

.. code-block:: text

    token:
        Token_String {
            printf("[Parser, string] %s\n", $1);

            [consumer parserDidParseString:$1];

            free($1);
        }
        | Token_Number {
            printf("[Parser, number] %d\n", $1);

            [consumer parserDidParseNumber:$1];
        }

Given our consumer (arbitrary Objective-C class, this is easy configurable by
Flex/Bison) is the following:

.. code-block:: objective-c

    @implementation ParserConsumer

    - (void)parserDidParseString:(char *)string {
        printf("[Consumer, string] %s\n", string);
    }

    - (void)parserDidParseNumber:(int)number {
        printf("[Consumer: number] %d\n", number);
    }

    @end

and given the input string is the:

.. code-block:: c

    char input[] = "RAINBOW UNICORN 1234 UNICORN";

    yy_scan_string(input, scanner);

    yyparse(scanner, parserConsumer);

here is the output we'll see from Xcode:

.. code-block:: text

    [Lexer, string] RAINBOW
    [Parser, string] RAINBOW
    [Consumer, string] RAINBOW
    [Lexer, string] UNICORN
    [Parser, string] UNICORN
    [Consumer, string] UNICORN
    [Lexer, number] 1234
    [Parser, number] 1234
    [Consumer: number] 1234
    [Lexer, string] UNICORN
    [Parser, string] UNICORN
    [Consumer, string] UNICORN
    <<EOF>>

Xcode has Flex/Bison out of box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It can be surprising but Xcode supports flex/bison out of the box. If you add
any Flex file with ``.lm`` extension (example: ``lexer.lm``) and any Bison file
with ``.ym`` extension (example: ``parser.lm``), Xcode will automatically start
compiling them without any other action from your side. Having those files you
can import Flex+Bison parser into your project's code:

.. code-block:: c

    #import "y.tab.h"

Note: file ``"y.tab.h"`` is parser file generated by default by Xcode in runtime
- it doesn't exists at first but it will be there as soon as your grammar files:
``lexer.lm`` and ``parser.ym`` are added to Xcode project and are compiled (they
are in Compile Sources of your target).

An example project: `A demo project showing the use of yacc and lex (bison,
flex) in a Xcode project <https://github.com/epatel/ParserTest>`_.

`HASM: toy assembler compiler <https://github.com/AlexDenisov/Hasm>`_ is also
based on this Xcode's feature.

However, there are two unfortunate limitations of Xcode:

First, Bison is GNU tool from OSX that Xcode uses is very old:

.. code-block:: bash

    $ bison --version
    bison (GNU Bison) 2.3
    Written by Robert Corbett and Richard Stallman.

    Copyright (C) 2006 Free Software Foundation, Inc.

This one is partially related to current limitation of Mac OS X itself: `What is
the reason for some of the Linux tools on OS X being so old? Is this related to
GPL licensing?
<https://www.quora.com/What-is-the-reason-for-some-of-the-Linux-tools-on-OS-X-being-so-old-Is-this-related-to-GPL-licensing>`_

Second, which is consequence of the first: it is not possible to make Flex/Bison
to work as reentrant parser (I did struggle to accomplish this using Xcode's
default Flex/Bison but didn't succeed because most of the tutorials for
reentrant parsers address newer versions of Bison).

The following describes what reentrant parser is and how to accomplish its setup
in Xcode project.

.. raw:: html

    <a name="Reentrant-parser"></a>

Reentrant parser
----------------

Both Flex and Bison are not reentrant (another word is "pure") by default.
Reentrance is closely related to thread safery. Due to their legacy history both
Flex and Bison use a bunch of global variables for their machinery so it is not
possible to run them in multi-threaded application because different threads
affect the same global state shared by instances of Flex and Bison. However they
both can be switched to "pure" mode:

Flex (from `19 Reentrant C Scanners
<http://flex.sourceforge.net/manual/Reentrant.html>`_):

    flex has the ability to generate a reentrant C scanner. This is accomplished
    by specifying %option reentrant (‘-R’) The generated scanner is both
    portable, and safe to use in one or more separate threads of control. The
    most common use for reentrant scanners is from within multi-threaded
    applications. Any thread may create and execute a reentrant flex scanner
    without the need for synchronization with other threads.

Bison (from `3.7.10 A Pure (Reentrant) Parser
<http://www.gnu.org/software/bison/manual/html_node/Pure-Decl.html>`_):

    A reentrant program is one which does not alter in the course of execution;
    in other words, it consists entirely of pure (read-only) code. Reentrancy is
    important whenever asynchronous execution is possible; for example, a
    nonreentrant program may not be safe to call from a signal handler. In
    systems with multiple threads of control, a nonreentrant program must be
    called only within interlocks.

    Normally, Bison generates a parser which is not reentrant. This is suitable
    for most uses, and it permits compatibility with Yacc. (The standard Yacc
    interfaces are inherently nonreentrant, because they use statically
    allocated variables for communication with yylex, including yylval and
    yylloc.)

Why would one need reentrant parser?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The use case is obvious: using multiple instances of parser to parse data in
parallel (can be BIG data that you want to speed up).

My use case is quite demonstrative: my toy terminal support tabs which means it
can have more than 1 connection to ttys. I don't want the parsers for those
connections to interfere with each other so this is where reentrancy kicks in:
each terminal window has corresponding thread with instance of parser based on
Flex/Bison, that parses input of its own terminal, reentrancy ensures that each
thread does parsing job in isolation from the other terminal threads.

Setup instructions
~~~~~~~~~~~~~~~~~~

The following is based on this example project: `Reentrant parser with Flex and
Bison
<https://github.com/stanislaw/Examples/tree/20160328-reentrant-parser-with-flex-and-bison>`_.
Feel free to clone it and see everything in detail.

Xcode project and folder Parser next to it:

.. code-block:: text

    ├── Parser
    │   ├── Makefile
    │   └── Source
    │       ├── Lexer.lm
    │       ├── Parser.ym
    │       └── ParserConsumer.h
    ├── README.md
    └── Reentrant-Parser-Using-Flex-and-Bison
        ├── Reentrant-Parser-Using-Flex-and-Bison
        │   └── main.m
        └── Reentrant-Parser-Using-Flex-and-Bison.xcodeproj

1. First of all get latest Flex and Bison:

.. code-block:: bash

    # `brew link` is needed to link against these new versions instead of default Xcode because both flex and bison are keg-only
    # See http://stackoverflow.com/questions/17015285/understand-homebrew-and-keg-only-dependencies for details
    #
    $ brew install flex && brew link flex --force
    $ brew install bison && brew link bison --force

    # Later it is important to explicitly specify full path:
    # /usr/local/bin/flex
    # /usr/local/bin/bison
    # because Xcode has its own environment with 10-year-old GNU tools enabled

    $ /usr/local/bin/flex --version
    flex 2.6.0
    $ /usr/local/bin/bison --version
    bison (GNU Bison) 3.0.4
    Written by Robert Corbett and Richard Stallman.

    Copyright (C) 2015 Free Software Foundation, Inc.
    ...

2. As described above we need to generate our lexer and parser outside of Xcode.
   I do this using Make:

.. code-block:: makefile

    PARSER_PATH=./Source
    PARSER_FILES=$(wildcard $(PARSER_PATH)/*)

    OUT_PATH=./Generated-Code

    generate: $(OUT_PATH)

    versions:
        /usr/local/bin/flex --version
        /usr/local/bin/bison --version

    clean:
        rm -rf $(OUT_PATH)

    $(OUT_PATH): $(PARSER_FILES)
        mkdir -p $(OUT_PATH)

        /usr/local/bin/flex --header-file=$(OUT_PATH)/Lexer.h --outfile=$(OUT_PATH)/Lexer.m $(PARSER_PATH)/Lexer.lm
        /usr/local/bin/bison --defines=$(OUT_PATH)/Parser.h --output=$(OUT_PATH)/Parser.m $(PARSER_PATH)/Parser.ym
        touch $(OUT_PATH)

To run:

.. code-block:: bash

    $ cd Parser && make

the resulting file structure (notice that Generated-Code folder appeared):

.. code-block:: text

    ├── Parser
    │   ├── Generated-Code
    │   │   ├── Lexer.h
    │   │   ├── Lexer.m
    │   │   ├── Parser.h
    │   │   └── Parser.m
    │   ├── Makefile
    │   └── Source
    │       ├── Lexer.lm
    │       ├── Parser.ym
    │       └── ParserConsumer.h
    ├── README.md
    └── Reentrant-Parser-Using-Flex-and-Bison
        ├── Reentrant-Parser-Using-Flex-and-Bison
        └── Reentrant-Parser-Using-Flex-and-Bison.xcodeproj

3. In Xcode, add ``Parser`` folder: make sure to **exclude Lexer.lm and
   Parser.ym** from your project's target otherwise Xcode will try to use its
   out-of-the-box Flex+Bison. Make sure to include the runtime-generated Lexer.m
   and Parser.m because those are your actual Parser.

4. Add ``make`` as a a `Build Phase
</images/2016-03-29-reentrant-parser-using-flex-and-bison/Example-Build-phases.png>`_.

5. Make some use your grammar. See how I do it with mine in example on Github:
`Reentrant parser with Flex and Bison: main.m
<https://github.com/stanislaw/Examples/blob/5a3c8d81c3ae4bbc896915ba12dafcc262debb3e/Reentrant-Parser-Using-Flex-and-Bison/Reentrant-Parser-Using-Flex-and-Bison/main.m>`_.

Gotchas
-------

It is extremely convenient to make Flex and Bison explicitly produce: 1) headers
along with code files 2) headers and code with good names.

Flex (Lexer.lm):

.. code-block:: text

    %option header-file = "./Generated Code/Lexer.h"
    %option outfile     = "./Generated Code/Lexer.m"

Bison (Parser.ym):

.. code-block:: text

    %output  "Generated Code/Parser.m"
    %defines "Generated Code/Parser.h"

The same can be done via command-line arguments - see the Makefile above.
Actually it makes more sense to keep these outside of Flex and Bison in Makefile
because it is implementation detail of how you integrate ``Parser`` to your
project.

This was the only way I could resolve all import conflicts (see next).

Import order is important
~~~~~~~~~~~~~~~~~~~~~~~~~

Otherwise one can run into all sorts of conflicts that arise from a circular
dependencies between Flex and Bison. The following order works for me:

Your code:

.. code-block:: objective-c

    #import "Parser.h"
    #import "Lexer.h"

Flex (Lexer.lm):

.. code-block:: text

    %{
    #import "Parser.h"
    %}

Bison (Parser.ym:

.. code-block:: text

    %{
    #import "Parser.h"
    #import "Lexer.h"
    %}

Demo projects
-------------

Non-reentrant parsers using default Xcode's Flex/Bison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`A demo project showing the use of yacc and lex (bison, flex) in a Xcode project
<https://github.com/epatel/ParserTest>`_

`HASM - Assembler for http://www.nand2tetris.org
<https://github.com/AlexDenisov/Hasm>`_

Reentrant parsers, normal command-line Flex/Bison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A very simple example using C and make: `Minimal re-entrant Flex/Bison
<https://github.com/blynn/symple/tree/75aaea79141a18a234c94dc8a2a7277d42fe83aa>`_

My example for usage inside Xcode project: `Reentrant parser with Flex and Bison
<https://github.com/stanislaw/Examples/tree/20160328-reentrant-parser-with-flex-and-bison>`_

Conclusion
----------

Configuration of both Flex and Bison can be quite a challenging task. In this
post I tried to collect the essentials of what I learned along the way:

- Avoiding Xcode's default magic for Flex/Bison. Instead getting the latest GNU
  versions and using good naming conventions for file names.
- Implementation of reentrancy for thread-safe parsing.

I hope this knowledge will help someone who might be learning the same topics as
I do.
