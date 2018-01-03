# Copyright (c) 2017, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
from typing import List

from ShExJSG import ShExJ

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

shex_2 = """{ "type":"Schema", "shapes": [
    { "id": "http://schema.example/PersonShape",
      "type":"Shape", "expression": {
        "id": "http://schema.example/nameExpr",
        "type": "TripleConstraint",
        "predicate": "http://xmlns.com/foaf/0.1/name"
      } },
    { "id": "http://schema.example/EmployeeShape",
      "type":"Shape", "expression": { "type": "TripleConstraint",
          "predicate": "http://schema.example/dependent",
          "valueExpr": "http://schema.example/PersonShape" } } ] }"""


def visit_1(v: List[ShExJ.shapeExprLabel], expr: ShExJ.shapeExpr) -> None:
    if 'id' in expr:
        v.append(expr.id)


class ShapeVisitorTestCase(unittest.TestCase):
    def test_example_1(self):
        from pyshex.utils.shape_visitor import ShapeVisitor
        schema, _ = setup_test(shex_1, None)
        visited = []
        ShapeVisitor(schema, schema.shapes[0].id, False).visit(visited, visit_1)
        self.assertEqual(["http://schema.example/EmployeeShape"], visited)

    def test_example_2(self):
        from pyshex.utils.shape_visitor import ShapeVisitor
        schema, _ = setup_test(shex_2, None)
        visited = []
        ShapeVisitor(schema, schema.shapes[1].id, True).visit(visited, visit_1)
        self.assertEqual(["http://schema.example/EmployeeShape", "http://schema.example/PersonShape" ], visited)


if __name__ == '__main__':
    unittest.main()
