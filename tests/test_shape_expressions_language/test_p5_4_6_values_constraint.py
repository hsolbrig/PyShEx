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

from rdflib.namespace import FOAF

from tests.utils.setup_test import rdf_header, setup_test, EX, gen_rdf

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
    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesValues
        schema, g = setup_test(shex_1, rdf_1)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesValues(g.value(EX.issue1, EX.state), nc))
        self.assertFalse(nodeSatisfiesValues(g.value(EX.issue2, EX.state), nc))

    def test_example_2(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesValues
        schema, g = setup_test(shex_2, rdf_2)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesValues(g.value(EX.issue3, FOAF.mbox), nc))
        self.assertTrue(nodeSatisfiesValues(g.value(EX.issue4, FOAF.mbox), nc))
        self.assertTrue(nodeSatisfiesValues(g.value(EX.issue5, FOAF.mbox), nc))
        self.assertFalse(nodeSatisfiesValues(g.value(EX.issue6, FOAF.mbox), nc))
        self.assertFalse(nodeSatisfiesValues(g.value(EX.issue7, FOAF.mbox), nc))

    def test_example_3(self):
        from pyshex.shape_expressions_language.p5_4_node_constraints import nodeSatisfiesValues
        schema, g = setup_test(shex_3, rdf_3)
        nc = schema.shapes[0].expression.valueExpr
        self.assertTrue(nodeSatisfiesValues(g.value(EX.issue8, FOAF.mbox), nc))
        self.assertTrue(nodeSatisfiesValues(g.value(EX.issue9, FOAF.mbox), nc))
        self.assertFalse(nodeSatisfiesValues(g.value(EX.issue10, FOAF.mbox), nc))


if __name__ == '__main__':
    unittest.main()
