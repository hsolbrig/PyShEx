import unittest

from rdflib import URIRef

from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesNumericFacet
from tests.utils.setup_test import setup_test, EX, rdf_header, gen_rdf

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://schema.example/confirmations",
      "valueExpr": { "type": "NodeConstraint", "mininclusive": 1 } } } ] }"""

rdf_1 = gen_rdf("""
:issue1 ex:confirmations 1 .
:issue2 ex:confirmations "2"^^xsd:byte .
:issue3 ex:confirmations 0 .
:issue4 ex:confirmations "ii"^^ex:romanNumeral .""")

shex_2 = """{
  "@context": "http://www.w3.org/ns/shex.jsonld",
  "type": "Schema",
  "shapes": [
    {
      "id": "http://a.example/S1",
      "type": "Shape",
      "expression": {
        "type": "TripleConstraint",
        "predicate": "http://a.example/p1",
        "valueExpr": {
          "type": "NodeConstraint",
          "nodeKind": "literal",
          "fractiondigits": 4
        }
      }
    }
  ]
}"""

rdf_2 = gen_rdf("""<http://a.example/s1> 
<http://a.example/p1> "1.23450"^^<http://www.w3.org/2001/XMLSchema#decimal> .""")


class NumericFacetTestCase(unittest.TestCase):
    def test_example_1(self):
        schema, g = setup_test(shex_1, rdf_1)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesNumericFacet(g.value(EX.issue1, EX.confirmations), nc))
        self.assertTrue(nodeSatisfiesNumericFacet(g.value(EX.issue2, EX.confirmations), nc))
        self.assertFalse(nodeSatisfiesNumericFacet(g.value(EX.issue3, EX.confirmations), nc))
        self.assertFalse(nodeSatisfiesNumericFacet(g.value(EX.issue4, EX.confirmations), nc))

    def test_trailing_zero(self):
        schema, g = setup_test(shex_2, rdf_2)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesNumericFacet(g.value(URIRef("http://a.example/s1"),
                                                          URIRef("http://a.example/p1")), nc))


if __name__ == '__main__':
    unittest.main()
