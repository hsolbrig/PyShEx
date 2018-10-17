# Python implementation of ShEx 2.0
[![Pyversions](https://img.shields.io/pypi/pyversions/PyShEx.svg)](https://pypi.python.org/pypi/PyShEx)

[![PyPi](https://version-image.appspot.com/pypi/?name=PyShEx)](https://pypi.python.org/pypi/PyShEx)


[![DOI](https://zenodo.org/badge/116042298.svg)](https://zenodo.org/badge/latestdoi/116042298)



This package is a reasonably literal implementation of the [Shape Expressions Language 2.0](http://shex.io/shex-semantics/).  It can parse and "execute" ShExC and ShExJ source.

## Revisions
* 0.2.dev3 -- added SchemaEvaluator and other tweaks.  There are still some unit tests that fail -- beware
* 0.3.0 -- Fix several issues.  Still does not pass all unit tests -- see `test_manifest.py` for details
* 0.4.0 -- Added sparql_slurper capabilities. 
* 0.4.1 -- Resolves several issues with reactome and disease test cases
* 0.4.2 -- Fix issues #13 (missing start) and #14 (Inconsistent shape causes loop)
* 0.4.3 -- Fix issues #16 and #15 and some refactoring
* 0.5.0 -- First cut at returning fail reasons... some work still needed
* 0.5.1 -- Update shexc parser to include multi-line comments and bug fixes
* 0.5.2 -- Issue with installer - missed the parse_tree package
* 0.5.3 -- make sparql_slurper a dependency
* 0.5.4 -- Fixed long recursion issue with blood pressure example
* 0.5.5 -- Fixed zero cardinality issue (#20)
* 0.5.6 -- Added CLI entry point and cleaned up error reporting
* 0.5.7 -- Throw an error on an invalid focus node (#23)
* 0.5.9 -- Candidate for ShEx 2.1

## Installation
```bash
pip install PyShEx
```
Note: If you need to escape single quotes in RDF literals, you will need to install the bleeding edge
of rdflib:
```bash
pip uninstall rdflib
pip install git+https://github.com/rdflib/rdflib
```
Unfortunately, however, `rdflib-jsonld` is NOT compatible with the bleeding edge rdflib, so you can't use a json-ld parser in this situation.

## evalshex CLI
```bash
> shexeval -h
usage: shexeval [-h] [-f FORMAT] [-s START] [-fn FOCUS] [-d] rdf shex

positional arguments:
  rdf                   Input RDF file
  shex                  ShEx specification

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Input RDF Format
  -s START, --start START
                        Start shape
  -fn FOCUS, --focus FOCUS
                        RDF focus node
  -d, --debug           Add debug output

```


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
Performance has been improved, but our current implementation of the `sparql_slurper` is entirely too fine-grained. Our
next steps include:
1) Get non-conformance reasons into the responses
2) Improve diagnostic and debugging tools
3) Add a time-out to catch really long evaluations
4) Adjust the slurper to pull larget chunks as needed and then refine on the retrieval end

This implementation passes all of the tests in the master branch of [validation/manifest.ttl](https://raw.githubusercontent.com/shexSpec/shexTest/master/validation/manifest.ttl) with the following exceptions:

At the moment, there are 1077 tests, of which:

* 970 pass
* 107 are skipped - reasons:
1) (52) sht:toldBNode, sht:LexicalBNode and sht:BNodeShapeLabel test non-blank blank nodes (`rdflib` does not preserve bnode "identity")
2) (24) sht:OutsideBMP -- test uses multi byte unicode (two aren't tagged)
3) (16) Uses ShEx 2.1 IMPORT feature -- not yet implemented (three aren't tagged)
5) (3) Focus is a Literal  -- not yet implemented
6) (5) Uses ShEx 2.1 INCLUDE feature -- not yet implemented
7) (3) Uses manifest shapemap feature -- not yet implemented
8) (2) sht:relativeIRI -- this isn't a real problem, but we havent taken time to deal with this in the test harness
9) (2) `rdflib` has a parsing error when escaping single quotes. (Issue submitted, awaiting release)

As mentioned above, at the moment this is as literal an implementation of the specification as was sensible.  This means, in particular, that we are less than clever when it comes to partition management.



## Notes
[manifest_tester.py](tests/utils/manifest_tester.py) is the current testing tool.  Once we get through the complete set of tests we'll create a command line tool and a UI

Note: At the moment we're just returning pass/fail.  We need to find documentation about what the return document should look like before we start returning detailed reports.

