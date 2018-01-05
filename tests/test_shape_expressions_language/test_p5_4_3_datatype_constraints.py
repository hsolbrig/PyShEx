import unittest

from rdflib import RDFS

from tests.utils.setup_test import rdf_header, setup_test, EX

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/IssueShape",
    "type": "Shape", "expression": {
      "type": "TripleConstraint", "predicate": "http://schema.example/submittedOn",
      "valueExpr": {
        "type": "NodeConstraint",
        "datatype": "http://www.w3.org/2001/XMLSchema#date"
      } } } ] }"""

rdf_1 = f"""{rdf_header}
:issue1 ex:submittedOn "2016-07-08"^^xsd:date .
:issue2 ex:submittedOn "2016-07-08T01:23:45Z"^^xsd:dateTime .
:issue3 ex:submittedOn "2016-07"^^xsd:date .
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

    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesDataType

        schema, g = setup_test(shex_1, rdf_1)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesDataType(g.value(EX.issue1, EX.submittedOn), nc))
        self.assertFalse(nodeSatisfiesDataType(g.value(EX.issue2, EX.submittedOn), nc))
        self.assertFalse(nodeSatisfiesDataType(g.value(EX.issue3b, EX.submittedOn), nc))

    @unittest.skipIf(True, "needs rdflib date parsing fix")
    def test_example_1a(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesDataType

        schema, g = setup_test(shex_1, rdf_1)
        nc = schema.shapes[0].expression.valueExpr
        self.assertFalse(nodeSatisfiesDataType(g.value(EX.issue3, EX.submittedOn), nc))
        self.assertFalse(nodeSatisfiesDataType(g.value(EX.issue3a, EX.submittedOn), nc))

    def test_example_2(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesDataType

        schema, g = setup_test(shex_2, rdf_2)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesDataType(g.value(EX.issue3, RDFS.label), nc))
        self.assertFalse(nodeSatisfiesDataType(g.value(EX.issue4, RDFS.label), nc))


if __name__ == '__main__':
    unittest.main()
