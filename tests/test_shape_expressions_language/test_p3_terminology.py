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

from rdflib import URIRef, Literal
from rdflib.namespace import FOAF

from tests.utils.setup_test import rdf_header, setup_test, EX, INST

rdf_1 = f"""{rdf_header}
inst:Issue1 
    ex:state      ex:unassigned ;
    ex:reportedBy ex:User2 .

ex:User2
    foaf:name     "Bob Smith" ;
    foaf:mbox     <mailto:bob@example.org> .
"""


class TerminologyTestCase(unittest.TestCase):

    def test_example_1(self):
        from pyshex.shape_expressions_language.p3_terminology import arcsOut, arcsIn, neigh

        _, g = setup_test(None, rdf_1)

        self.assertEqual({
            (EX.User2, FOAF.mbox, URIRef('mailto:bob@example.org')),
            (EX.User2, FOAF.name, Literal('Bob Smith'))},
            arcsOut(g, EX.User2))
        self.assertEqual({
            (INST.Issue1, EX.reportedBy, EX.User2)},
            arcsIn(g, EX.User2))
        
        self.assertEqual({
            (EX.User2, FOAF.mbox, URIRef('mailto:bob@example.org')),
            (EX.User2, FOAF.name, Literal('Bob Smith')),
            (INST.Issue1, EX.reportedBy, EX.User2)},
            neigh(g, EX.User2))

    def test_predicates(self):
        from pyshex.shape_expressions_language.p3_terminology import predicatesIn, predicatesOut, predicates
        _, g = setup_test(None, rdf_1)
        self.assertEqual({FOAF.mbox, FOAF.name}, predicatesOut(g, EX.User2))
        self.assertEqual({EX.reportedBy}, predicatesIn(g, EX.User2))
        self.assertEqual({FOAF.mbox, FOAF.name, EX.reportedBy}, predicates(g, EX.User2))


if __name__ == '__main__':
    unittest.main()
