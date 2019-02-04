import unittest
from typing import List

from rdflib.namespace import FOAF

from pyshex.parse_tree.parse_node import ParseNode
from pyshex.shape_expressions_language.p5_context import Context
from tests.utils.setup_test import rdf_header, EX, gen_rdf, setup_context

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/NoActionIssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://schema.example/state",
      "valueExpr": {
        "type": "NodeConstraint", "values": [
          "http://schema.example/Resolved",
          "http://schema.example/Rejected" ] } } } ] }"""

rdf_1 = f"""{rdf_header}
:issue1 ex:state ex:Resolved .
:issue2 ex:state ex:Unresolved .
"""

shex_2 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/EmployeeShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://xmlns.com/foaf/0.1/mbox",
      "valueExpr": {
        "type": "NodeConstraint", "values": [
          {"value": "N/A"},
          { "type": "IriStemRange", "stem": "mailto:engineering-" },
          { "type": "IriStemRange", "stem": "mailto:sales-", "exclusions": [
              { "type": "IriStem", "stem": "mailto:sales-contacts" },
              { "type": "IriStem", "stem": "mailto:sales-interns" }
            ] }
        ] } } } ] }"""

rdf_2 = gen_rdf("""<issue3> foaf:mbox "N/A" .
<issue4> foaf:mbox <mailto:engineering-2112@a.example> .
<issue5> foaf:mbox <mailto:sales-835@a.example> .
<issue6> foaf:mbox "missing" .
<issue7> foaf:mbox <mailto:sales-contacts-999@a.example> .""")

shex_3 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/EmployeeShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint",
      "predicate": "http://xmlns.com/foaf/0.1/mbox",
      "valueExpr": {
        "type": "NodeConstraint", "values": [
          { "type": "IriStemRange", "stem": {"type": "Wildcard"},
            "exclusions": [
              { "type": "IriStem", "stem": "mailto:engineering-" },
              { "type": "IriStem", "stem": "mailto:sales-" }
            ] }
        ] } } } ] }"""

rdf_3 = gen_rdf("""<issue8> foaf:mbox 123 .
<issue9> foaf:mbox <mailto:core-engineering-2112@a.example> .
<issue10> foaf:mbox <mailto:engineering-2112@a.example> .""")


class ValuesConstraintTestCase(unittest.TestCase):
    @staticmethod
    def fail_reasons(cntxt: Context) -> List[str]:
        return [e.strip() for e in cntxt.current_node.fail_reasons(cntxt.graph)]

    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesValues

        cntxt = setup_context(shex_1, rdf_1)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.issue1, EX.state)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesValues(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue2, EX.state)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesValues(cntxt, focus, nc))
        self.assertEqual(['Node: :Unresolved not in value set:\n'
                          '\t {"values": ["http://schema.example/Resolved", "http://schema...'],
                         self.fail_reasons(cntxt))

    def test_example_2(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesValues

        cntxt = setup_context(shex_2, rdf_2)
        nc = cntxt.schema.shapes[0].expression.valueExpr

        focus = cntxt.graph.value(EX.issue3, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesValues(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue4, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesValues(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue6, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesValues(cntxt, focus, nc))
        self.assertEqual(['Node: "missing" not in value set:\n'
                         '\t {"values": [{"value": "N/A"}, {"stem": "mailto:engineering-"...'],
                         self.fail_reasons(cntxt))

        focus = cntxt.graph.value(EX.issue7, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesValues(cntxt, focus, nc))
        self.assertEqual(['Node: <mailto:sales-contacts-999@a.example> not in value set:\n'
                          '\t {"values": [{"value": "N/A"}, {"stem": "mailto:engineering-"...'],
                         self.fail_reasons(cntxt))

    def test_example_3(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesValues

        cntxt = setup_context(shex_3, rdf_3)
        nc = cntxt.schema.shapes[0].expression.valueExpr
        focus = cntxt.graph.value(EX.issue8, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesValues(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue9, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertTrue(nodeSatisfiesValues(cntxt, focus, nc))

        focus = cntxt.graph.value(EX.issue10, FOAF.mbox)
        cntxt.current_node = ParseNode(nodeSatisfiesValues, nc, focus, cntxt)
        self.assertFalse(nodeSatisfiesValues(cntxt, focus, nc))
        self.assertEqual(['Node: <mailto:engineering-2112@a.example> not in value set:\n'
                          '\t {"values": [{"stem": {"type": "Wildcard"}, "exclusions": [{"...'],
                         self.fail_reasons(cntxt))


if __name__ == '__main__':
    unittest.main()
