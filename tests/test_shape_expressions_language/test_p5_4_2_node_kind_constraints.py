import unittest
from typing import List

from pyshex.parse_tree.parse_node import ParseNode
from pyshex.shape_expressions_language.p5_context import Context
from tests.utils.setup_test import rdf_header, EX, setup_context

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint", "predicate": "http://schema.example/state",
      "valueExpr": { "type": "NodeConstraint", "nodeKind": "iri" } } } ] }"""

rdf_1 = f"""{rdf_header}
:issue1 ex:state ex:HunkyDory .
:issue2 ex:taste ex:GoodEnough .
:issue3 ex:state "just fine" .
"""


class NodeKindConstraintTest(unittest.TestCase):

    @staticmethod
    def fail_reasons(cntxt: Context) -> List[str]:
        return [e.strip() for e in cntxt.current_node.fail_reasons(cntxt.graph)]

    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesNodeKind
        cntxt = setup_context(shex_1, rdf_1)

        nc = cntxt.schema.shapes[0].expression.valueExpr

        focus = cntxt.graph.value(EX.issue1, EX.state)
        cntxt.current_node = ParseNode(nodeSatisfiesNodeKind, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesNodeKind(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue3, EX.state)
        cntxt.current_node = ParseNode(nodeSatisfiesNodeKind, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesNodeKind(cntxt, focus, nc))
        self.assertEqual(['Node kind mismatch have: Literal expected: iri'], self.fail_reasons(cntxt))

if __name__ == '__main__':
    unittest.main()
