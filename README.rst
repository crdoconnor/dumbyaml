Dumb YAML
=========

Dumb YAML is a a restricted YAML parser for python with an emphasis
on cutting out the "smart" features that can cause surprise and
inhibit readability.

* Everything parsed as a string, list or dict. There's no implicit typing. yes == "yes" != True.
* JSONesque flow style YAML ( x: { a: 1, b: 2 } ) is explicitly disallowed.
* Typing tag tokens (!!bool / !!str / !!float) are explicitly disallowed.
* Node anchors and references are explicitly disallowed.

See :doc:`/comparisons/YAML` for a more direct comparison with regular YAML.

DumbYAML was built for use with the
`hitch testing framework's <https://hitchtest.com/>`_
`test description language <https://hitchtest.readthedocs.org/en/latest/glossary/hitch_test_description_language.html>`_.

Tested on Python 2.6.6, 2.7.10, 3.2.1 and 3.5.0


Usage
-----

It's built atop pyyaml (which is a dependency) and has the same API.

If you are already using pyyaml you don't have to change a lot.

Install::

   pip install dumbyaml

Use::

    >>> import dumbyaml
    >>> dumbyaml.load("x: 1\ny: 2")
    {'y': '2', 'x': '1'}

Disallowed features raise YAMLError (the default pyyaml exception)::

    >>> dumbyaml.load("x: &anchor")
    Traceback (most recent call last):
      raise AnchorTokenDisallowed(token)
    dumbyaml.AnchorTokenDisallowed: AnchorToken(value='anchor')

Then, anywhere where you are using data parsed from YAML into
a list, dict, list of dicts or dict of lists or whatever,
you will need to add an *explicit* type conversion in your
code from the string to your desired type.

E.g::

    is_it_null = None if yamlresult['isnull'].lower() == "null" else yamlresult['isnull']
    answer_to_question = yamlresult['answer'].lower() in ("yes", "y", "true")
    number_of_twinkies = int(yamlresult['Number of twinkies'])
    cost_of_space_station = float(yamlresult['Cost of space station'])


Why?
----

YAML is arguably the tersest, cleanest markup language for marking up
hierarchical data. It handles lists, associations and block literals
beautifully and readably with a minimalist syntax.

It's a fantastic language for encoding configuration data, or,
indeed, declarative data of any kind.

However, the "smarter" features are often confusing and make
YAML both scary for non-programmers and ugly for programmers.

As Tim Berners Lee said::

    Computer Science spent the last forty years making languages which
    were as powerful as possible. Nowadays we have to appreciate the reasons
    for picking not the most powerful solution but the least powerful.

And, as Guido van Rossum said::

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Readability counts.
    There should be one-- and preferably only one --obvious way to do it.


What do I substitute for those features if I was already using them?
--------------------------------------------------------------------

* The implicit type conversions can be replaced by explicit type conversions in your code.
* Flow style can be replaced by block style.
* Node anchors that made your YAML DRY can be replaced by a templating language like jinja2.
* Binary encoding (!!binary) can be replaced by base64 and an explicit type conversion.


Removing implicit typing is great but what YAML really needs is *stronger* typing
---------------------------------------------------------------------------------

That's what `pykwalify <https://github.com/Grokzen/pykwalify/>`_ is for.


This is why you should use XML/JSON/TOML/INI/etc. instead!
----------------------------------------------------------

Since cleanliness and readability are somewhat a matter of opinion
and the after-effects of choosing a markup language is not always
clear up front, objective side by side comparisons are probably
the best way of letting people make the right choice.

If you feel tempted to start a flamewar over your favorite
markup language, please channel your anger into creating
a side by side comparison, forking this repo and issuing a
pull request. Thanks!

Rules:

* Put the differentiating features at the top.
* Present the trade offs as objectively as you can.
* Side by side comparisons must represent the same data.

Comparisons:

* Regular :doc:`/comparisons/YAML`

Hacking
-------

If you want to hack, you can TDD with::

  sudo pip install hitch
  cd dumbyaml/tests
  hitch init
  hitch test run.test

The py.test unit tests are in dumbyaml/unittests.
