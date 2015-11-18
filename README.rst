Dumb YAML
=========

Dumb YAML is a restricted YAML parser that removes the 'smart' features
and relacing YAML's weak implicit typing with strong explicit typing.

It mostly has the same API as pyyaml.

Examples::

    >>> str(yaml.load("x: yes")['x'])
    True
    >>> str(dumbyaml.load("x: yes")['x'])
    "yes"
    
    >>> bool(yaml.load("x: yes")['x'])
    True
    >>> bool(dumbyaml.load("x: yes")['x'])
    True
    
    >>> int(yaml.load("x: yes")['x'])
    1
    >>> int(dumbyaml.load("x: yes")['x'])
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "yamlnode.py", line 153, in __int__
        raise InvalidYAMLTypeConversion(self.item.__repr__(), "int")
    dumbyaml.exceptions.InvalidYAMLTypeConversion: Conversion not possible of 'yes' to int

The disallowed YAML features which inhibit readability are:

* JSONesque flow style YAML ( x: { a: 1, b: 2 } ) is explicitly disallowed::

  x: { a: 1, b: 2 }

* Tag tokens (!!bool / !!str / !!float) are explicitly disallowed::

  x: !!str yes

* Node anchors and references are explicitly disallowed::

  a: &node1
      t: 1
      r: 1
  b: *node1
  
Using any of these will raise an exception.

DumbYAML was built for use with the
`hitch testing framework's <https://hitchtest.com/>`_
`test description language <https://hitchtest.readthedocs.org/en/latest/glossary/hitch_test_description_language.html>`_.

(It is not currently used yet though).

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

Disallowed features raise an exception inheriting from YAMLError (the default pyyaml exception)::

    >>> dumbyaml.load("x: &anchor")
    Traceback (most recent call last):
      raise AnchorTokenDisallowed(token)
    dumbyaml.AnchorTokenDisallowed: AnchorToken(value='anchor')

You will need to add explicit type conversions in your code. E.g.::

    answer_to_question = bool(yamlresult['answer'])
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
YAML both scary for non-programmers and ugly for programmers and its
weak implicit typing is confusing.

As Tim Berners Lee said::

    Computer Science spent the last forty years making languages which
    were as powerful as possible. Nowadays we have to appreciate the reasons
    for picking not the most powerful solution but the least powerful.

And, as Tim Peters said in the Zen of Python::

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Readability counts.
    There should be one-- and preferably only one --obvious way to do it.

More about less powerful languages:

* `The Principle of Least Power by Jeff Atwood <https://blog.codinghorror.com/the-principle-of-least-power/>``_
* `We need less powerful languages by Luke Plant <http://lukeplant.me.uk/blog/posts/less-powerful-languages/>`_

Hacking
-------

If you want to hack, you can TDD with::

  sudo pip install hitch
  cd dumbyaml/tests
  hitch init
  hitch test *.test

.. _YAML: comparisons/YAML.rst
