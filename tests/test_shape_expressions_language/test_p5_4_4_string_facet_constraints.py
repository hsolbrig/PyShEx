import re
import unittest

from ShExJSG import ShExJ
from pyjsg.jsglib import jsg
from rdflib import Graph, URIRef

from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesStringFacet
from tests.utils.setup_test import rdf_header, setup_test, EX

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

pattern = re.sub(r'\\', r'\\\\', '^\\t\\\\𝒸\?$')
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

    def test_example_1(self):
        schema, g = setup_test(shex_1, rdf_1)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesStringFacet(g.value(EX.issue1, EX.submittedBy), nc))
        self.assertFalse(nodeSatisfiesStringFacet(g.value(EX.issue2, EX.submittedBy), nc))

    def test_example_2(self):
        schema, g = setup_test(shex_2, rdf_2)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesStringFacet(g.value(EX.issue6, EX.submittedBy), nc))
        self.assertFalse(nodeSatisfiesStringFacet(g.value(EX.issue7, EX.submittedBy), nc))

    def test_example_3(self):
        schema, g = setup_test(shex_3, rdf_3)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesStringFacet(g.value(EX.product6, EX.trademark), nc))
        self.assertTrue(nodeSatisfiesStringFacet(g.value(EX.product7, EX.trademark), nc))
        self.assertFalse(nodeSatisfiesStringFacet(g.value(EX.product8, EX.trademark), nc))


if __name__ == '__main__':
    unittest.main()
