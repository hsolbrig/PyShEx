import unittest

from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesNumericFacet
from tests.utils.setup_test import setup_test, EX, rdf_header

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://schema.example/confirmations",
      "valueExpr": { "type": "NodeConstraint", "mininclusive": 1 } } } ] }"""

rdf_1 = f"""{rdf_header}
:issue1 ex:confirmations 1 .
:issue2 ex:confirmations "2"^^xsd:byte .
:issue3 ex:confirmations 0 .
:issue4 ex:confirmations "ii"^^ex:romanNumeral ."""


class NumericFacetTestCase(unittest.TestCase):
    def test_example_1(self):
        schema, g = setup_test(shex_1, rdf_1)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesNumericFacet(g.value(EX.issue1, EX.confirmations), nc))
        self.assertTrue(nodeSatisfiesNumericFacet(g.value(EX.issue2, EX.confirmations), nc))
        self.assertFalse(nodeSatisfiesNumericFacet(g.value(EX.issue3, EX.confirmations), nc))
        self.assertFalse(nodeSatisfiesNumericFacet(g.value(EX.issue4, EX.confirmations), nc))


if __name__ == '__main__':
    unittest.main()
