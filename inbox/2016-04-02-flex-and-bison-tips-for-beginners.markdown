---
layout: post
title: "Flex and Bison: tips for beginners"
date: 2016-04-02T22:50:21+02:00

keywords: flex, bison, flex-lexer, scanner, tokenizer, reentrant, thread-safe, xcode
description: Unordered collection of Flex and Bison tips for beginners. 

---

This is unordered collection of Flex and Bison tips that might be helpful for beginners. Each problem is unique so this collection, derived from my experience with Flex and Bison, is not comprehensive, anyway I want to share these tips as something that I would like to have learned in first place when I started learning Flex and Bison myself.

This post complements another post: [Reentrant parser using Flex and Bison](/2016/03/29/reentrant-parser-using-flex-and-bison.html). If you need reentrant Flex and Bison and especially if you use Xcode make sure to read that post as well.

So let's start!

### Disable default rule

Taken from [Flex Directives](http://people.cs.aau.dk/~marius/sw/flex/Flex-Directives.html), this one is must:

> Die with an error message on unmatched characters instead of echoing them. We advise you not to rely on the default rule for sake of completeness, therefore, you should always use it to find holes in your rules. 
   
### Enabling lexer's 'debug' option can be quite helpful

Taken from [Flex Directives](http://people.cs.aau.dk/~marius/sw/flex/Flex-Directives.html). Author recommends avoiding printf however I still use it quite often, this probably depends on grammar:

`%option debug`

> Produce a scanner which can be traced. This introduce a variable, yy_flex_debug, which, when set to a non zero value, triggers tracing messages on the standard error output.

> You are encouraged to use this option, in particular when developing your scanner, and to have some option to set yy_flex_debug. In particular, never write printf-like tracing code in your scanner: that's an absolute waste of time. 

### Flex can be very sensitive to syntax

There are places where Flex is very strict on syntax. I now have it as a rule of thumb: if I am getting Flex errors over and over on something that should work I always double-check syntax or experiment with it.

#### Comments

In Flex you cannot have comments starting from the beginning of line. This is vaguely described in [5.4 Comments in the Input](http://flex.sourceforge.net/manual/Comments-in-the-Input.html), I now always use 2 spaces indentation.

#### Start condition scopes

This aspect of Flex's sensitivity to syntax is not documented in [10 Start Conditions](http://flex.sourceforge.net/manual/Start-Conditions.html): if you want to have start condition scope, you must not have space between `<YOUR_CONDITION>` and opening {:

    %x YOUR_CONDITION

      //    no space!
      //       \/
    <YOUR_CONDITION>{
        "\\n"   return '\n';
        "\\r"   return '\r';
        "\\f"   return '\f';
        "\\0"   return '\0';
    }

## Advanced tips

### Reentrant aka thread-safe parser

I have written the whole post around this topic: [Reentrant parser using Flex and Bison](http://stanislaw.github.io/2016/03/29/reentrant-parser-using-flex-and-bison.html). 

### Working with continous scanning stream (like socket)

**TLDR;** redefine `YY_INPUT` macro. 

For details see these two topics: [How to detect partial unfinished token and join its pieces that are obtained from two consequent portions of input?](http://stackoverflow.com/questions/36242886/how-to-detect-partial-unfinished-token-and-join-its-pieces-that-are-obtained-fro?lq=1) and [Flex, continuous scanning stream (from socket). Did I miss something using yywrap()?](http://stackoverflow.com/questions/23979378/flex-continuous-scanning-stream-from-socket-did-i-miss-something-using-yywra?lq=1).

## Examples

Examples that I found especially helpful can be found at the end of [Reentrant parser using Flex and Bison](http://stanislaw.github.io/2016/03/29/reentrant-parser-using-flex-and-bison.html). There is one that I created myself.

## Conclusion

I hope this knowledge will help someone who might be learning the same topics as I do.

