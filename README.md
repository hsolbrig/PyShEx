# Python implementation of ShEx 2.0
[![Pyversions](https://img.shields.io/pypi/pyversions/PyShEx.svg)](https://pypi.python.org/pypi/PyShEx)

[![PyPi](https://version-image.appspot.com/pypi/?name=PyShEx)](https://pypi.python.org/pypi/PyShEx)

This package is a reasonably literal implementation of the [Shape Expressions Language 2.0](http://shex.io/shex-semantics/).  It can parse and "execute" ShExC and ShExJ source.

## Revisions
* 0.2.dev3 -- added SchemaEvaluator and other tweaks.  There are still some unit tests that fail -- beware
* 0.3.0 -- Fix several issues.  Still does not pass all unit tests -- see `test_manifest.py` for details

## Installation
```bash
pip install ShEx
```
Note: If you need to escape single quotes in RDF literals, you will need to install the bleeding edge
of rdflib:
```bash
pip uninstall rdflib
pip install git+https://github.com/rdflib/rdflib
```
Unfortunately, however, `rdflib-jsonld` is NOT compatible with the bleeding edge rdflib, so you can't use a json-ld parser in this situation.

## General Layout
The root `pyshex` package is subdivided into:

* [shape_expressions_language](pyshex/shape_expressions_language) - implementation of the various sections in  [Shape Expressions Language 2.0](http://shex.io/shex-semantics/).  As an example, [3. Terminology](http://shex.io/shex-semantics/#terminology) is implemented in [p3_terminology.py](pyshex/shape_expressions_language/p3_terminology.py), [5.2 Validation Definition](http://shex.io/shex-semantics/#validation) in [p5_2_validation_definition.py](pyshex/shape_expressions_language/p5_2_validation_definition.py), etc.
* [shapemap_structure_and_language](pyshex/shapemap_structure_and_language) - implementation of [ShapeMap Structure and Language](http://shex.io/shape-map/) (as well as we can understand it)
* [sparql11_query](pyshex/sparql11_query) - required sections from [SPARQL 1.1 Query Language section 17.2](https://www.w3.org/TR/sparql11-query/#operandDataTypes)
* [utils](pyshex/utils) - supporting utilities

The ShEx schema definitions for this package come from [ShExJSG](https://github.com/hsolbrig/ShExJSG)

We are trying to keep the python as close as possible to the (semi-)formal specification.  As an example, the statement:
```text
Se is a ShapeAnd and for every shape expression se2 in shapeExprs, satisfies(n, se2, G, m)
``` 
is implemented in Python as:
```python
        ...
if isinstance(se, ShExJ.ShapeAnd):
    return satisfiesShapeAnd(cntxt, n, se)
        ...
def satisfiesShapeAnd(cntxt: Context, n: nodeSelector, se: ShExJ.ShapeAnd) -> bool:
    return all(satisfies(cntxt, n, se2) for se2 in se.shapeExprs)
```

## Dependencies
This package is built using:
* [ShExJSG](https://github.com/hsolbrig/ShExJSG) -- an object representation of the ShEx AST as defined by [ShEx.jsg](https://github.com/shexSpec/shexTest/blob/master/doc/ShExJ.jsg) and compiled through the [PyJSG](https://github.com/hsolbrig/pyjsg) compiler.
* The python [ShExC](https://github.com/shexSpec/grammar/tree/master/parsers/python) compiler -- which transforms the [Shape Expressions Language](http://shex.io/shex-semantics/index.html) into ShExJSG images.
* [rdflib](https://rdflib.readthedocs.io/en/stable/) 

## Current status
This implementation passes all of the tests in the master branch of [validation/manifest.ttl](https://raw.githubusercontent.com/shexSpec/shexTest/master/validation/manifest.ttl) with the following exceptions:

At the moment, there are 1077 tests, of which:

* 967 pass
* 110 are skipped - reasons:
2) (1) Extraneous 'id' field for Schema (2.1 feature?)
3) (1) Takes too long -- we need to beef up the partition generator
4) (4) Test uses IMPORT -- not implemented in ShEx 2.0, and not tagged as such
5) (2) Test uses multi-byte literals aren't tagged as such
7) (2) sht:BNodeShapeLabel - rdflib doesn't preserve bnodes
8) (13) sht:Import - test uses V2.1 IMPORT feature
9) (5) sht:Include ...
10) (30) sht:LexicalBNode - test counts on preservation of BNODES
11) (22) sht:OutsideBMP -- test uses multi byte unicode
12) (3) sht:ShapeMap ...
13) (20) sht:ToldBNode
14) (2) sht:relativeIRI -- this isn't a real problem, but we havent taken time to deal with this in the test harness


We've also skipped two tests:
* `skipped` - the ShEx schema has an `id` in the outermost level, which fails the parser
* `repeated-group` - this tests the limits of our naive partition algorithm.

As mentioned above, at the moment this is as literal an implementation of the specification as was sensible.  This means, in particular, that we are less than clever when it comes to partition management.



## Notes
[test_manifest_entry.py](tests/utils/manifest_tester.py) is the current testing tool.  Once we get through the complete set of tests we'll create a command line tool and a UI

Note: At the moment we're just returning pass/fail.  We need to find documentation about what the return document should look like before we start returning detailed reports.

