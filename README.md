# Python implementation of ShEx 2.0
This package is a reasonably literal implementation of the [Shape Expressions Language 2.0](http://shex.io/shex-semantics/).

The root `pyshex` package is subdivided into:

* [shape_expressions_language](pyshex/shape_expressions_language) - implementation of the various sections in  [Shape Expressions Language 2.0](http://shex.io/shex-semantics/).  As an example, [3. Terminology](http://shex.io/shex-semantics/#terminology) is implemented in [p3_terminology.py](pyshex/shape_expressions_language/p3_terminology.py), [5.2 Validation Definition](http://shex.io/shex-semantics/#validation) in [p5_2_validation_definition.py](pyshex/shape_expressions_language/p5_2_validation_definition.py), etc.
* [shapemap_structure_and_language](pyshex/shapemap_structure_and_language) - implementation of [ShapeMap Structure and Language](http://shex.io/shape-map/)
* [sparql11_query](pyshex/sparql11_query) - required sections from [SPARQL 1.1 Query Language section 17.2](https://www.w3.org/TR/sparql11-query/#operandDataTypes)
* [utils](pyshex/utils) - supporting utils

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
We are currently working through the tests that are defined in the [shexTest](https://github.com/shexSpec/shexTest/) [validation](https://github.com/shexSpec/shexTest/tree/master/validation) directory.

At the moment, we can pass all of the tests in the manifest up to `1dotOne2dot_pass_p1`, with the following exceptions:

1) BNode name matching tests -- rdflib does not preserve BNode identifiers, so these tests are not possible.
2) `1datatype_pass` -- this uses a non-sparql datatype and the spec says that this does not have to pass.
3) RDF literals with single quotes and escaped internal quotes -- this bug was reported and (I though) fixed in rdflib, but apparently it didn't take.
4) Double values of '0E0' and '0e0' - rdflib doesn't parse this representation.
5) 1literalPattern_with_ascii_boundaries -- this is so crazy that I can't even read it in my browser.  We'll cope with insane UTF-16 codes after we get the rest of this stuff done
6) A number of fraction digits tests where the tests just appear to be broken.  As an example, `1literalFractiondigits_pass-decimal-short` asserts that  
```text
<http://a.example/s1> 
<http://a.example/p1> 
"1.2345"^^<http://www.w3.org/2001/XMLSchema#decimal> .
```

should pass
```text
<http://a.example/S1> {
   <http://a.example/p1> LITERAL FRACTIONDIGITS 5
}
```
(What am I missing?)


## Notes
[test_manifest_entry.py](tests/test_shextest_validation/test_manifest_entry.py) is the current testing tool.  Once we get through the complete set of tests we'll create a command line tool and a UI

Note: At the moment we're just returning pass/fail.  We need to find documentation about what the return document should look like before we start returning detailed reports.

