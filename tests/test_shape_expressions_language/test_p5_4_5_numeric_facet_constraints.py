import unittest

from rdflib import URIRef

from pyshex.parse_tree.parse_node import ParseNode
from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesNumericFacet
from tests.utils.setup_test import EX, gen_rdf, setup_context

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
        cntxt = setup_context(shex_1, rdf_1)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.issue1, EX.confirmations)
        cntxt.current_node = ParseNode(nodeSatisfiesNumericFacet, nc, focus)
        self.assertTrue(nodeSatisfiesNumericFacet(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.issue2, EX.confirmations)
        cntxt.current_node = ParseNode(nodeSatisfiesNumericFacet, nc, focus)
        self.assertTrue(nodeSatisfiesNumericFacet(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.issue3, EX.confirmations)
        cntxt.current_node = ParseNode(nodeSatisfiesNumericFacet, nc, focus)
        self.assertFalse(nodeSatisfiesNumericFacet(cntxt, focus, nc))
        self.assertEqual(['Numeric value volation - minimum inclusive: 1 actual: 0'], cntxt.current_node.fail_reasons())

    def test_trailing_zero(self):
        cntxt = setup_context(shex_2, rdf_2)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(URIRef("http://a.example/s1"), URIRef("http://a.example/p1"))
        cntxt.current_node = ParseNode(nodeSatisfiesNumericFacet, nc, focus)
        self.assertTrue(nodeSatisfiesNumericFacet(cntxt, focus, nc))


if __name__ == '__main__':
    unittest.main()
