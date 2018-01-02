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
