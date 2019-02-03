import re
import unittest
from typing import List

from pyshex.parse_tree.parse_node import ParseNode
from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesStringFacet
from pyshex.shape_expressions_language.p5_context import Context
from tests.utils.setup_test import rdf_header, EX, setup_context

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://schema.example/submittedBy",
      "valueExpr": { "type": "NodeConstraint", "minlength": 10 } } } ] }
"""

rdf_1 = f"""{rdf_header}
:issue1 ex:submittedBy <http://a.example/bob> .
:issue2 ex:submittedOn "bob" ."""

shex_2 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://schema.example/submittedBy",
      "valueExpr": { "type": "NodeConstraint",
                     "pattern": "genuser[0-9]+", "flags": "i" }
} } ] }"""

rdf_2 = f"""{rdf_header}
:issue6 ex:submittedBy :genUser218 .
:issue7 ex:submittedBy :genContact817 ."""

pattern = re.sub(r'\\', r'\\\\', r'^\t\\𝒸\?$')
shex_3 = f"""{{ "type": "Schema", "shapes": [
  {{ "id": "http://schema.example/ProductShape",
    "type": "Shape", "expression": {{
      "type": "TripleConstraint",
      "predicate": "http://schema.example/trademark",
      "valueExpr": {{ "type": "NodeConstraint",
                     "pattern": "{pattern}" }}
}} }} ] }}"""

# Warning - the editor has to preserve the tab in product6 - if it changes it to spaces, no match
rdf_3 = f"""{rdf_header}
:product6 ex:trademark "\\t\\\\𝒸?" .
:product7 ex:trademark "\\t\\\\\U0001D4B8?" .
:product8 ex:trademark "\\t\\\\\\\\U0001D4B8?" .

"""


class StringFacetTestCase(unittest.TestCase):

    @staticmethod
    def fail_reasons(cntxt: Context) -> List[str]:
        return [e.strip() for e in cntxt.current_node.fail_reasons(cntxt.graph)]

    def test_example_1(self):
        cntxt = setup_context(shex_1, rdf_1)
        nc = cntxt.schema.shapes[0].expression.valueExpr

        focus = cntxt.graph.value(EX.issue1, EX.submittedBy)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesStringFacet(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.issue2, EX.submittedBy)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesStringFacet(cntxt, focus, nc))
        self.assertEqual(['String length violation - minimum: 10 actual: 4'], self.fail_reasons(cntxt))

    def test_example_2(self):
        cntxt = setup_context(shex_2, rdf_2)
        nc = cntxt.schema.shapes[0].expression.valueExpr

        focus = cntxt.graph.value(EX.issue6, EX.submittedBy)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesStringFacet(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.issue7, EX.submittedBy)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesStringFacet(cntxt, focus, nc))
        self.assertEqual(['Pattern match failure - pattern: genuser[0-9]+ flags:i string: '
                          'http://schema.example/genContact817'], self.fail_reasons(cntxt))

    def test_example_3(self):
        cntxt = setup_context(shex_3, rdf_3)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.product6, EX.trademark)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesStringFacet(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.product7, EX.trademark)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesStringFacet(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.product8, EX.trademark)
        cntxt.current_node = ParseNode(nodeSatisfiesStringFacet, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesStringFacet(cntxt, focus, nc))
        self.assertEqual(['Pattern match failure - pattern: ^\\t\\\\𝒸\\?$ flags:None string: \t'
                          '\\\\U0001D4B8?'], self.fail_reasons(cntxt))


if __name__ == '__main__':
    unittest.main()
