import unittest
from typing import List

from rdflib import RDFS

from pyshex.parse_tree.parse_node import ParseNode
from pyshex.shape_expressions_language.p5_context import Context
from tests.utils.setup_test import rdf_header, EX, setup_context

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint", "predicate": "http://schema.example/submittedOn",
      "valueExpr": {
        "type": "NodeConstraint",
        "datatype": "http://www.w3.org/2001/XMLSchema#dateTime"
      } } } ] }"""

rdf_1 = f"""{rdf_header}
:issue1 ex:submittedOn "2016-07-08T01:23:45Z"^^xsd:dateTime .
:issue2 ex:submittedOn "2016-07-08"^^xsd:date .
:issue3 ex:submittedOn "2016-07-08T01:23:45Zz"^^xsd:dateTime .
:issue3a ex:submittedOn "2016-07a"^^xsd:date .
:issue3b ex:submittedOn "a2016-07"^^xsd:date .
"""

shex_2 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://www.w3.org/2000/01/rdf-schema#label",
      "valueExpr": {
        "type": "NodeConstraint",
        "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString"
      } } } ] }"""

rdf_2 = f"""{rdf_header}
:issue3 rdfs:label "emits dense black smoke"@en .
:issue4 rdfs:label "unexpected odor" .
"""


class DataTypeTestCase(unittest.TestCase):

    @staticmethod
    def fail_reasons(cntxt: Context) -> List[str]:
        return [e.strip() for e in cntxt.current_node.fail_reasons(cntxt.graph)]

    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesDataType

        cntxt = setup_context(shex_1, rdf_1)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.issue1, EX.submittedOn)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesDataType(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.issue2, EX.submittedOn)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesDataType(cntxt, focus, nc))
        self.assertEqual(['Datatype mismatch - expected: http://www.w3.org/2001/XMLSchema#dateTime '
                          'actual: http://www.w3.org/2001/XMLSchema#date'], self.fail_reasons(cntxt))

        focus = cntxt.graph.value(EX.issue3b, EX.submittedOn)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesDataType(cntxt, focus, nc))
        self.assertEqual(['Datatype mismatch - expected: http://www.w3.org/2001/XMLSchema#dateTime '
                          'actual: http://www.w3.org/2001/XMLSchema#date'], self.fail_reasons(cntxt))

    @unittest.skipIf(True, "needs rdflib date parsing fix")
    def test_example_1a(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesDataType

        cntxt = setup_context(shex_1, rdf_1)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.issue3, EX.submittedOn)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesDataType(cntxt, focus, nc))
        focus = cntxt.graph.value(EX.issue3a, EX.submittedOn)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesDataType(cntxt, focus, nc))

    def test_example_2(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesDataType

        cntxt = setup_context(shex_2, rdf_2)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.issue3, RDFS.label)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesDataType(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue4, RDFS.label)
        cntxt.current_node = ParseNode(nodeSatisfiesDataType, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesDataType(cntxt, focus, nc))
        self.assertEqual(['Datatype mismatch - expected: '
                          'http://www.w3.org/1999/02/22-rdf-syntax-ns#langString actual: '
                          'http://www.w3.org/2001/XMLSchema#string'], self.fail_reasons(cntxt))


if __name__ == '__main__':
    unittest.main()
