import unittest

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

    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesNodeKind

        cntxt = setup_context(shex_1, rdf_1)

        nc = cntxt.schema.shapes[0].expression.valueExpr
        # TODO: figure out how to get reason into this
        self.assertTrue(nodeSatisfiesNodeKind(cntxt, cntxt.graph.value(EX.issue1, EX.state), nc))
        self.assertFalse(nodeSatisfiesNodeKind(cntxt, cntxt.graph.value(EX.issue3, EX.state), nc))


if __name__ == '__main__':
    unittest.main()
