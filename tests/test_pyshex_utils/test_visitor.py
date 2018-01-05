import unittest
from typing import List

from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p5_context import Context
from tests.utils.setup_test import setup_test

shex_1 = """{ "type": "Schema", "shapes": [
  { "id": "http://schema.example/EmployeeShape",
    "type": "Shape", "expression": {
      "type": "EachOf", "expressions": [
        "http://schema.example/nameExpr",
        { "type": "TripleConstraint",
          "predicate": "http://schema.example/empID",
          "valueExpr": { "type": "NodeConstraint",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer" } } ] } },
  { "id": "http://schema.example/PersonShape",
    "type": "Shape", "expression": {
      "id": "http://schema.example/nameExpr",
      "type": "TripleConstraint",
      "predicate": "http://xmlns.com/foaf/0.1/name" } } ] }"""

shex_2 = """{
  "@context": "http://www.w3.org/ns/shex.jsonld",
  "type": "Schema",
  "shapes": [
    {
      "id": "http://all.example/S1",
      "type": "ShapeNot",
      "shapeExpr": "http://all.example/S2"
    },
    {
      "id": "http://all.example/S2",
      "type": "Shape",
      "expression": {
        "type": "TripleConstraint",
        "id": "http://all.example/S2e",
        "predicate": "http://all.example/p1",
        "min": 0,
        "max": 1,
        "valueExpr": "http://all.example/S2"
      }
    }
  ]
}"""


def visit_shape(v: List[ShExJ.shapeExprLabel], expr: ShExJ.shapeExpr, _:Context) -> None:
    if 'id' in expr and expr.id is not None:
        v.append(expr.id)


def visit_te(v: List[ShExJ.tripleExprLabel], expr: ShExJ.shapeExpr, _:Context) -> None:
    if 'id' in expr and expr.id is not None:
        v.append(expr.id)


class VisitorTestCase(unittest.TestCase):
    def test_example_1(self):
        schema, _ = setup_test(shex_1, None)
        cntxt = Context(None, schema)
        shapes_visited = []
        triples_visited = []
        cntxt.visit_shapes(schema.shapes[0], visit_shape, shapes_visited)
        self.assertEqual(["http://schema.example/EmployeeShape"], shapes_visited)

    @unittest.skipIf(True, "Example 2 may not be valid - check it")
    def test_example_2(self):
        schema, _ = setup_test(shex_2, None)
        cntxt = Context(None, schema)
        shapes_visited = []
        triples_visited = []
        cntxt.visit_shapes(schema.shapes[0], visit_shape, shapes_visited)
        self.assertEqual(["http://schema.example/S1", "http://schema.example/S2" ], shapes_visited)


if __name__ == '__main__':
    unittest.main()
