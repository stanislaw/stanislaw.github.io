How to build a static iOS framework and distribute it as a Component using Make
===============================================================================

:date: 2015-11-23 10:53:34
:modified: 2015-11-23 10:53:34
:tags: iOS, Make
:category: Posts
:slug: 2015-11-23-how-to-build-static-framework-using-make
:summary: This post is a complement to introductory post about Components: bare-bones dependency management system.

This post is a complement to introductory post
`Components: taking a step back from Dependency Management <http://lowlevelbits.org/components-management>`_
about the
`Components <https://github.com/AlexDenisov/Components>`_:
bare-bones dependency management system that was recently introduced to our iOS
community by `AlexDenisov <https://github.com/AlexDenisov>`_.
Components go even further than Carthage by providing you with a complete control
over how you manage your dependencies.

It is strongly recommended to read that introductory post first as this post
targets Components and shows how a maintainer of a static iOS framework can
easily build his Framework and distribute it as a Component using Make.

Why Make?
---------

`@fogus on Twitter <https://twitter.com/fogus/status/526740537823735808>`_:

    Make is the worst build system ever created except for every other build system created after Make.

`@natpryce on Twitter <https://twitter.com/natpryce/status/556381696174874624>`_:

    Those who don't know Make are doomed to repeat it.

`Another twit by @natpryce <https://twitter.com/natpryce/status/526755049155088384>`_:

    @fogus treat make as a parallel, pure-functional dataflow programming language and it remains pretty manageable in my experience.

According to Wikipedia initial release of Make was made in "1977, 38 years ago". Without a doubt it is the most widespread, stable and still very simple system so actually it is not really that many of choices that we have for our bare-bones style of dependency management with Components.

I personally have been using Bash scripts to manage my build scripts but thanks
to Alex Denisov, I learned about caching capabilities of Make which shine when
used inside Components infrastructure: if you already downloaded the zip file
of third-party library you do not download it again as longer it is cached,
if you already unzipped that file you will not unzip it again, because Make
knows that it is there, if you copied that library's final artefacts to your
project you will not be copying them over and over again and all that results,
to say it using marketing words, in blazing fast performance of your build
scripts given Components were cached once. Aside from this caching feature,
Make itself is very fast – even if you run ``./components.sh install`` the first
time, it works much faster than for example ``pod install`` as those all .make
files are just direct bare-bone instructions on how to fetch, compile and copy
your third-party libraries in a way that those library require.
This becomes especially impressive when you run your project on CI where cached
Components are installed just immediately.

Instead of crafting artifical example I have rather decided to show how I use
Make to maintain my own library:
`CompositeOperations <https://github.com/stanislaw/CompositeOperations>`_.

CompositeOperations is distributed as static framework so I also recommend
reading the following topic on StackOverflow where
`Petr Korolev <https://github.com/skywinder>`_ and I explain how to create an
iOS Static Framework:
`How to export “fat” Cocoa Touch Framework (for Simulator and Device)? <http://stackoverflow.com/questions/29634466/how-to-export-fat-cocoa-touch-framework-for-simulator-and-device/31270427#31270427>`_.

Building a static iOS framework
-------------------------------

Here is working version of Makefile that I currently use to create iOS Static
Framework from CompositeOperations. As it is always with build scripts they are
subject to change but still this version is stable enough and works for us during
latest releases of CompositeOperations:
`CompositeOperations/Makefile.iOS <https://github.com/stanislaw/CompositeOperations/blob/2fdbbbd6216d8838092de085608f1e0a2f257f52/Makefile.iOS>`_.

.. code-block:: makefile

    # Makefile.iOS
    NAME=CompositeOperations
    XCODEPROJ=DevelopmentApp/DevelopmentApp.xcodeproj
    CONFIGURATION=Release
    SCHEME=CompositeOperations-iOS
    SIMULATOR='platform=iOS Simulator,name=iPhone 6s Plus'

    FRAMEWORK_FOLDER=$(NAME).framework

    ### Paths

    BUILD_PATH=$(PWD)/Build
    BUILD_PATH_SIMULATOR=$(BUILD_PATH)/$(CONFIGURATION)-iphonesimulator
    BUILD_PATH_IPHONE=$(BUILD_PATH)/$(CONFIGURATION)-iphoneos
    BUILD_PATH_UNIVERSAL=$(BUILD_PATH)/$(CONFIGURATION)-universal
    BUILD_PATH_UNIVERSAL_FRAMEWORK_FOLDER=$(BUILD_PATH_UNIVERSAL)/$(FRAMEWORK_FOLDER)
    BUILD_PATH_UNIVERSAL_FRAMEWORK_BINARY=$(BUILD_PATH_UNIVERSAL_FRAMEWORK_FOLDER)/$(NAME)

    DISTRIBUTION_PATH=$(PWD)/Distribution
    ZIPBALL_NAME=$(NAME)-iOS.zip
    ZIPBALL_PATH=$(DISTRIBUTION_PATH)/$(ZIPBALL_NAME)

    ### Colors

    RESET=\033[0;39m
    RED=\033[0;31m
    GREEN=\033[0;32m

    ### Actions

    .PHONY: all archive clean test build validate zip

    default: test

    archive: test build validate zip

    test:
        xcodebuild -project $(XCODEPROJ) \
            -scheme $(SCHEME) \
            -sdk iphonesimulator \
            -destination $(SIMULATOR) \
            clean test

    build:
        xcodebuild -project $(XCODEPROJ) \
            -scheme $(SCHEME) \
            -sdk iphonesimulator \
            -destination $(SIMULATOR) \
            -configuration $(CONFIGURATION) \
            CONFIGURATION_BUILD_DIR=$(BUILD_PATH_SIMULATOR) \
            clean build

        xcodebuild -project $(XCODEPROJ) \
            -scheme $(SCHEME) \
            -sdk iphoneos \
            -configuration $(CONFIGURATION) \
            CONFIGURATION_BUILD_DIR=$(BUILD_PATH_IPHONE) \
            clean build

        rm -rf $(BUILD_PATH_UNIVERSAL)
        mkdir -p $(BUILD_PATH_UNIVERSAL)

        cp -Rv $(BUILD_PATH_IPHONE)/$(FRAMEWORK_FOLDER) $(BUILD_PATH_UNIVERSAL)
        lipo $(BUILD_PATH_SIMULATOR)/$(FRAMEWORK_FOLDER)/$(NAME) $(BUILD_PATH_IPHONE)/$(FRAMEWORK_FOLDER)/$(NAME) -create -output $(BUILD_PATH_UNIVERSAL_FRAMEWORK_BINARY)

    validate: validate.i386 validate.x86_64 validate.armv7 validate.arm64

    validate.%:
        @printf "Validating $*... "
        @lipo -info $(BUILD_PATH_UNIVERSAL_FRAMEWORK_BINARY) | grep -q '$*' && echo "$(GREEN)Passed$(RESET)" || (echo "$(RED)Failed$(RESET)"; exit 1)

    zip:
        mkdir -p $(DISTRIBUTION_PATH)
        cd $(BUILD_PATH_UNIVERSAL) && zip -r -FS $(DISTRIBUTION_PATH)/$(ZIPBALL_NAME) $(FRAMEWORK_FOLDER)

    clean:
        rm -rf $(BUILD_PATH)
        rm -rf $(DISTRIBUTION_PATH)

Creating a Component
--------------------

Here is corresponding ``.make`` file that is intended to be used by a consumer
of ComponentOperations as a Component:
`CompositeOperations/Components.make/CompositeOperations.make <https://github.com/stanislaw/CompositeOperations/blob/2fdbbbd6216d8838092de085608f1e0a2f257f52/Components.make/CompositeOperations.make>`_.
Give it a look before reading further.

If convention: ``Components.make/CompositeOperations.make`` is not clear I
recommend re-reading introductory post about Components one more time:
`Components: taking a step back from Dependency Management <http://lowlevelbits.org/components-management>`_.

Most of the following should be self explanatory, I will just comment on things
that are relevant to Components infrastructure:

.. code-block:: makefile

    # Components.make/CompositeOperations.make
    NAME=CompositeOperations
    VERSION=0.8.5

    GH_REPO=stanislaw/CompositeOperations
    ZIPBALL_URL=https://github.com/$(GH_REPO)/releases/download/$(VERSION)/CompositeOperations-iOS.zip

    ### Paths

    COMPONENTS_BUILD_CACHE_PATH ?= $(HOME)/Library/Caches/Components
    COMPONENTS_INSTALL_PATH ?= ./Components

These two "global" variables ``COMPONENTS_BUILD_CACHE_PATH`` and
``COMPONENTS_INSTALL_PATH`` are to be inherited from parent ``components.sh``
script who exports them, but "?=" is used to still allow running this
``.make`` file in isolation from parent Components infrastructure.

.. code-block:: makefile

    COMPONENT_BUILD_PATH=$(COMPONENTS_BUILD_CACHE_PATH)/$(NAME)
    COMPONENT_SOURCE_PATH=$(COMPONENT_BUILD_PATH)/$(NAME)-$(VERSION)
    COMPONENT_FRAMEWORK_PATH=$(COMPONENT_SOURCE_PATH)/$(NAME).framework

    COMPONENT_INSTALL_PATH=$(COMPONENTS_INSTALL_PATH)/$(NAME)

    ZIPBALL_PATH=$(COMPONENT_BUILD_PATH)/$(NAME)-$(VERSION).zip

    ### Targets

    .PHONY: install update uninstall clean prepare purge

    install: $(COMPONENT_INSTALL_PATH)

    uninstall:
        rm -rf $(COMPONENT_INSTALL_PATH)

    update: uninstall install

    clean:
        rm -rf $(COMPONENT_SOURCE_PATH)
        rm -rf $(ZIPBALL_PATH)

    purge: uninstall clean

    ### Artefacts

    $(COMPONENT_INSTALL_PATH): $(COMPONENT_SOURCE_PATH)
        mkdir -p $(COMPONENT_INSTALL_PATH)
        cp -Rv $(COMPONENT_FRAMEWORK_PATH) $(COMPONENT_INSTALL_PATH)

    $(COMPONENT_SOURCE_PATH): $(ZIPBALL_PATH)
        unzip $(ZIPBALL_PATH) -d $(COMPONENT_SOURCE_PATH)

    $(ZIPBALL_PATH): $(COMPONENT_BUILD_PATH)
        wget --no-use-server-timestamps $(ZIPBALL_URL) -O $(ZIPBALL_PATH)

    $(COMPONENT_BUILD_PATH):
        mkdir -p $(COMPONENT_BUILD_PATH)

In the lines that follow the ``### Targets`` comment all targets rely on
"caching capability" of Make - when we run ``make install`` targets are evaluated
in reverse order like:

``COMPONENT_INSTALL_PATH (depends on) -> COMPONENT_SOURCE_PATH (depends on) -> ZIPBALL_PATH (depends on) -> COMPONENT_BUILD_PATH``.

When Make finds that a particular target's dependency's target's path exists
and its modification time is not greater than that target's path modification
time, it does skip that step by not performing any real action. So for example
if we already downloaded CompositeOperations-iOS.zip file which corresponds to
``ZIPBALL_PATH``, Make will not try to download it again. This is why we use
``wget --no-use-server-timestamps`` to make sure that ``ZIPBALL_PATH`` will
always be newer than modification date of its dependency:
``COMPONENT_BUILD_PATH`` target which is created on preceding step. Or another
example: if ``$(COMPONENT_INSTALL_PATH)`` folder already exists, then Make will
not perform any action at all. This caching capability of Make allows
Components.sh script from introductory article to work **very fast** given we
have all our Components build cache in place in the
``~/Library/Caches/Components`` folder.

Conclusion
----------

This post is one of the very first examples of how Make can be used inside
Components infrastructure. Now we are looking forward to hear back from the
community if Make will work for all of us at massive scale. Try creating your
own Component.make and see it in action.
