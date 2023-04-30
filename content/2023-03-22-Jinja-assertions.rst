Assertions in Jinja templates
=============================

:date: 2023-03-22 10:20
:modified: 2023-03-22 10:20
:tags: Python
:category: Posts
:slug: 2023-03-22-jinja-assertions
:summary: One way of implementing assertions in Jinja templates.

This post captures one way of implementing assertions in Jinja templates. The
assertion mechanism is inspired by this StackOverflow answer: `How to raise an
exception in a Jinja2 macro? <https://stackoverflow.com/a/24789436/598057>`_ and
is based on the `Jinja Extensions feature
<https://jinja.palletsprojects.com/en/latest/extensions>`_.

The following code becomes possible in Jinja template:

.. code-block:: jinja

    {%- assert variable is string -%}
    {%- assert
      link.__class__.__name__ == "FileReference",
      "Expected FileReference, got: "~link
    -%}

Jinja `supports a number of checks
<https://jinja.palletsprojects.com/en/latest/templates/#list-of-builtin-tests>`_,
all of which are usable with this approach.

The code of the extension is as follows.

.. code-block:: python

    from typing import Any, Optional

    from jinja2 import (
        Environment,
        FileSystemLoader,
        StrictUndefined,
        TemplateRuntimeError,
        nodes,
    )
    from jinja2.ext import Extension

    from strictdoc import environment


    # The solution was inspired by the StackOverflow question:
    # How to raise an exception in a Jinja2 macro?
    # https://stackoverflow.com/questions/21778252
    class AssertExtension(Extension):
        # This is our keyword(s):
        tags = {"assert"}

        def __init__(self, environment):  # pylint: disable=redefined-outer-name
            super().__init__(environment)
            self.current_line = None
            self.current_file = None

        def parse(self, parser):
            lineno = next(parser.stream).lineno
            self.current_line = lineno
            self.current_file = parser.filename

            condition_node = parser.parse_expression()
            if parser.stream.skip_if("comma"):
                context_node = parser.parse_expression()
            else:
                context_node = nodes.Const(None)

            return nodes.CallBlock(
                self.call_method(
                    "_assert", [condition_node, context_node], lineno=lineno
                ),
                [],
                [],
                [],
                lineno=lineno,
            )

        def _assert(
            self, condition: bool, context_or_none: Optional[Any], caller
        ):  # pylint: disable=unused-argument
            if not condition:
                error_message = (
                    f"Assertion error in the Jinja template: "
                    f"{self.current_file}:{self.current_line}."
                )
                if context_or_none:
                    error_message += f" Message: {context_or_none}"
                raise TemplateRuntimeError(error_message)
            return ""


    jinja_environment = Environment(
        loader=FileSystemLoader("path-to-templates"),
        undefined=StrictUndefined,
        extensions=[AssertExtension],
    )

    # use jinja_environment...

Note that in this code, ``StrictUndefined`` is also used to make Jinja raise
exceptions when an undefined variable is referenced from a Jinja template. The
assertions build the next level of more precise checks on top of
``StrictUndefined``.

I have come to the idea of writing this extension because of several visual
regressions that I found in `my project
<https://github.com/strictdoc-project/strictdoc>`_. Without assertions, a number
of errors can be easily introduced in Jinja templates, and these errors can be
quite difficult to detect.

I would be happy to learn about your experience with making Jinja a safer markup
language. Feel free to `drop me a line <mailto:s.pankevich@gmail.com>`_.
