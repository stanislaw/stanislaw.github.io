---
layout: post
title: "xcodebuild: how to really change its build path"
date: 2016-02-28T21:16:21+01:00

keywords: ios,testing,xcode,xcodebuild
description: "This is short one-solution-post that is longer version of my answer to StackOverflow topic: Separate build directory using xcodebuild"

---

This is short one-solution-post that is longer version of my answer to this StackOverflow topic: [Separate build directory using xcodebuild](http://stackoverflow.com/questions/4969932/separate-build-directory-using-xcodebuild).

**Background:** I build my tests from both Xcode and command line.

**Problem:** If I run my tests with `Command + U` and then I run them with `make test`, the build artifacts of test suite built from Xcode become overriden so that next time I run `Command + U` my test target will be built from scratch again. The benefits of incremental compilation are lost for both modes as both kinds of test runs override each other.

**Solution:** Completely isolate build artefacts that are created by command-line builds from corresponding build artefacts created by Xcode when tests are run from within Xcode.

<br/>

My naive approach to solve this problem was to redirect xcodebuild to another `CONFIGURATION_BUILD_DIR` like:

```
xcodebuild ... CONFIGURATION_BUILD_DIR=./Build-command-line
```

However it turned out that xcodebuild had some build settings that were not controlled by this variable i.e. Xcode was still building some of its artefacts to its default `./Build` folder. So I needed to investigate on details of `xcodebuild -showBuildSettings` to understand how to make xcodebuild to build everything to desired `./Build-command-line` folder. I used 

    xcodebuild -scheme MyScheme -showBuildSettings | grep Build\/


to find all build settings that correspond to all build paths and by trial-end-error I found "the generative" build settings that are enough to redirect all build artefacts produced by xcodebuild to custom folder.

I ended up using the following command:


    BUILD_DIR=./Build-command-line
    DERIVED_DATA_DIR=$(BUILD_DIR)/DerivedData

    xcodebuild -project MyProject.xcodeproj \
               -IDEBuildOperationMaxNumberOfConcurrentCompileTasks=`sysctl -n hw.ncpu` \
               -scheme MyScheme \
               -sdk iphonesimulator \
               -destination 'platform=iOS Simulator,name=iPhone 6S Plus,OS=latest' \
               -xcconfig command-line-build.xcconfig \
               -derivedDataPath $(DERIVED_DATA_DIR) \
               test

Where `command-line-build.xcconfig` is:

    /// This xcconfig is used to make Xcode build all of its artefacts to a
    /// custom folder. Use it for command line builds so that their caches
    /// do not interfere with the caches of normal builds from inside Xcode.
    ///
    /// To make most sense of the following configuration you should also redirect
    /// path to derived data using xcodebuild parameter:
    /// xcodebuild ...-derivedDataPath $(DERIVED_DATA_DIR)...
    /// where $(DERIVED_DATA_DIR) also points to Build-command-line/DerivedData
    ///
    /// Tested against Xcode 7.3.1 (7D1014)
    ///
    /// Source: xcodebuild: how to really change its build path
    /// http://stanislaw.github.io/2016/02/28/xcodebuild-how-to-really-change-its-build-path.html

    HERE_BUILD=$(SRCROOT)/Build-command-line
    HERE_INTERMEDIATES=$(HERE_BUILD)/Intermediates

    /// Paths
    /// the following paths are enough to redirect everything to $HERE_BUILD
    MODULE_CACHE_DIR    = $(HERE_BUILD)/DerivedData/ModuleCache
    OBJROOT             = $(HERE_INTERMEDIATES)
    SHARED_PRECOMPS_DIR = $(HERE_INTERMEDIATES)/PrecompiledHeaders
    SYMROOT             = $(HERE_BUILD)/Products

Having this setup I can now use both `Command + U` and `make test` (which is `make test_unit && make test_integration && make test_functional` done by Make) - they are now built in two separate directories and that makes a very good speed-up in build time of both.

P.S. Of course `xcodebuild`'s build settings are subject to change however as of `Xcode Version 7.3.1 (7D1014)` this solution works very well.

See also my post: [Test Automation for iOS](http://tech.blacklane.com/2015/12/13/test-automation-for-ios/).
