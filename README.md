# Python implementation of ShEx 2.0
This package is a reasonably literal implementation of the [Shape Expressions Language 2.0](http://shex.io/shex-semantics/).

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

## Current status
This implementation passes all of the tests in the master branch of [validation/manifest.ttl](https://raw.githubusercontent.com/shexSpec/shexTest/master/validation/manifest.ttl) with the following exceptions:

At the moment, there are 1077 tests, of which:

* 932 pass
* 145 skipped

1) BNode name matching tests -- rdflib does not preserve BNode identifiers, so these tests are not possible.
2) RDF literals with single quotes and escaped internal quotes -- this bug was reported and (I though) fixed in rdflib, but apparently it didn't take.
3) Double values of '0E0' and '0e0' - rdflib doesn't parse this representation.
4) Relative URI's - we're running this test locally and haven't figured out all of the bits of rewrite we have to do.  
5) Carriage Returns -- the rdflib parser reads a newline as '\n' instead of '\r\n', so embedded carriage return matches fail.
6) There is no JSON representation of ".shextern" files
7) Test uses a 2.1 feature (IMPORTS)
8) There are a number of files (all starting with "1NOT", curiously) that do not have JSON representations in the [schemas directory](https://github.com/shexSpec/shexTest/tree/master/schemas).

We've also skipped two tests:
* `skipped` - the ShEx schema has an `id` in the outermost level, which fails the parser
* `repeated-group` - this tests the limits of our naive partition algorithm.

As mentioned above, at the moment this is as literal an implementation of the specification as was sensible.  This means, in particular, that we are less than clever when it comes to partition management.



## Notes
[test_manifest_entry.py](tests/test_shextest_validation/test_manifest_entry.py) is the current testing tool.  Once we get through the complete set of tests we'll create a command line tool and a UI

Note: At the moment we're just returning pass/fail.  We need to find documentation about what the return document should look like before we start returning detailed reports.

