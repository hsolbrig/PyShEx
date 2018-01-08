# Copyright (c) 2018, Mayo Clinic
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

from rdflib import Literal

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFTriple, RDFGraph
from tests.utils.setup_test import EX, gen_rdf, setup_test

rdf_1 = gen_rdf("""
<issue1> ex:submittedOn "2016-07-08"^^xsd:date .
<issue2> ex:submittedOn "2016-07-08T01:23:45Z"^^xsd:dateTime .
<issue3> ex:submittedOn "2016-07"^^xsd:date .""")


rdf_out = """@prefix ns1: <http://schema.example/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ns1:issue1 ns1:submittedOn "2016-07-08"^^xsd:date .

ns1:issue2 ns1:submittedOn "2016-07-08T01:23:45+00:00"^^xsd:dateTime .

ns1:issue3 ns1:submittedOn "2016-07-01"^^xsd:date .

"""


class NotationAndTerminologyTestCase(unittest.TestCase):
    def test_rdf_triple(self):
        x = RDFTriple((EX.issue1, EX.num, Literal(17)))
        self.assertEqual(EX.issue1, x.s)
        self.assertEqual(EX.num, x.p)
        self.assertEqual(17, x.o.value)
        self.assertEqual("<http://schema.example/issue1> <http://schema.example/num> 17 .",
                         str(x))

    def test_rdf_graph(self):
        x = RDFGraph([(EX.issue1, EX.count, Literal(17))])
        self.assertEqual(1, len(x))
        x = RDFGraph([(EX.issue1, EX.count, Literal(17)), (EX.issue1, EX.count, Literal(17))])
        self.assertEqual(1, len(x))
        x = RDFGraph([(EX.issue1, EX.count, Literal(17)), RDFTriple((EX.issue1, EX.count, Literal(17)))])
        self.assertEqual(1, len(x))
        _, g = setup_test(None, rdf_1)
        x = RDFGraph(g)
        self.assertEqual(rdf_out, str(x))


if __name__ == '__main__':
    unittest.main()
