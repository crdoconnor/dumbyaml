Dumb YAML vs Regular YAML
=========================

Aimed at
--------

Representing hierarchical and relational data in a readable way.


Distinguishing features
-----------------------

Dumb YAML is just YAML except:

* Everything parsed as a string, list or dict. There is *no implicit typing* (e.g. yes == "yes" != True).
* Flow style YAML ( { } [ ] ) is explicitly disallowed (e.g. x: {a: 1, b: 2} )
* Node anchors and references are explicitly disallowed (e.g. x: * or a: &)

Trade offs
----------

No implicit typing means fewer surprise type conversions. Example::

  >>> document = """
  - Don Corleone: Do you have faith in my judgement?
  - Clemenza: Yes
  - Don Corleone: Do I have your loyalty?
  - Clemenza: Yes, always Godfather.
  """
  >>> yaml.load(document)
  [{'Don Corleone': 'Do you have faith in my judgement?'},
   {'Clemenza': True},
   {'Don Corleone': 'Do I have your loyalty?'},
   {'Clemenza': 'Yes, always Godfather.'}]
  >>> dumbyaml.load(document)
  [{'Don Corleone': 'Do you have faith in my judgement?'},
   {'Clemenza': 'Yes'},
   {'Don Corleone': 'Do I have your loyalty?'},
   {'Clemenza': 'Yes, always Godfather.'}]


No implicit typing also means extra code is required to explicitly convert YAML strings to integers, bools, dates, etc::

  document = """
  Nitrogen:
    Code: 3
    Element: yes
  """
  >>> int(dumbyaml.load(document)['Nitrogen']['Code'])
  3
  >>> bool(dumbyaml.load(document)['Nitrogen']['Element'])
  True

No flow style means that the syntax is simpler, easier to read and the { and } are less likely to
be mixed up with { and } used by Jinja2, or any other templating language::

    x: { a: {{ whats }}, b: {{ going }}, c: {{ on }} }

No node anchors means nothing like this ::

    x: &x 12
    y: *x

In regular YAML that equals {"x": 12, y: "12"}. I didn't even know this *was* a feature until
I started this project. It's to DRY your markup code I suppose. I prefer to use templating languages
for this purpose.
