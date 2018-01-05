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
