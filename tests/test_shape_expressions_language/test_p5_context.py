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
import json
from typing import List

from ShExJSG import ShExJ
from rdflib import URIRef, RDF

from pyshex.shape_expressions_language.p5_context import Context
from pyshex.utils.schema_utils import predicates_in_expression
from tests.utils.setup_test import gen_rdf, setup_context

shex_1 = """
{ "type": "Schema",
  "shapes": [
     { "id": "http://schema.example/UserShape",
       "type": "Shape",
       "extra": ["http://www.w3.org/1999/02/22-rdf-syntax-ns#type"],
       "expression": { "type": "TripleConstraint",
         "id" : "http://schema.example/te1",
         "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
         "valueExpr": { "type": "NodeConstraint",
                        "values": ["http://schema.example/Teacher"]
                      }
       }
     }
  ]
}"""

rdf_1 = gen_rdf(""" <Alice> ex:shoeSize "30"^^xsd:integer .
<Alice> a ex:Teacher .
<Alice> a ex:Person .
<SomeHat> ex:owner <Alice> .
<TheMoon> ex:madeOf <GreenCheese> .""")


def predicate_finder(predicates: List[URIRef], expr: ShExJ.shapeExpr, cntxt: Context) -> None:
    if isinstance(expr, ShExJ.Shape) and expr.expression is not None:
        if isinstance(expr.expression, ShExJ.TripleConstraint):
            predicates.append(URIRef(expr.expression.predicate))
        elif isinstance(expr.expression, ShExJ.tripleExprLabel):
            predicates.append(URIRef(cntxt.tripleExprFor(expr.expression).predicate))
        

class ContextTestCase(unittest.TestCase):
    def test_basic_context(self):
        c = setup_context(shex_1, rdf_1)
        self.assertEqual(['http://schema.example/UserShape'], list(c.schema_id_map.keys()))
        self.assertTrue(isinstance(list(c.schema_id_map.values())[0], ShExJ.Shape))
        self.assertEqual(['http://schema.example/te1'], list(c.te_id_map.keys()))
        self.assertTrue(isinstance(list(c.te_id_map.values())[0], ShExJ.TripleConstraint))
        
    def test_predicate_scan(self):
        c = setup_context(shex_1, rdf_1)
        predicates: List[URIRef] = []
        c.visit_shapes(c.shapeExprFor('http://schema.example/UserShape'), predicate_finder, predicates)
        self.assertEqual([RDF.type], predicates)
        # Quick test of the utility function
        self.assertEqual(predicates_in_expression(c.shapeExprFor('http://schema.example/UserShape'), c),
                         [ShExJ.IRIREF(str(u)) for u in predicates])



if __name__ == '__main__':
    unittest.main()
