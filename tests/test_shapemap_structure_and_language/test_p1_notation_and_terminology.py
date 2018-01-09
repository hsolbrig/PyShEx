import unittest

from rdflib import Literal

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFTriple, RDFGraph
from tests.utils.setup_test import EX, gen_rdf, setup_test

rdf_1 = gen_rdf("""
<issue1> ex:submittedOn "2016-07-08"^^xsd:date .
<issue2> ex:submittedOn "2016-07-08T01:23:45Z"^^xsd:dateTime .
<issue3> ex:submittedOn "2016-07"^^xsd:date .""")


rdf_out = """ns1:issue1 ns1:submittedOn "2016-07-08"^^xsd:date .

ns1:issue2 ns1:submittedOn "2016-07-08T01:23:45+00:00"^^xsd:dateTime .

ns1:issue3 ns1:submittedOn "2016-07-01"^^xsd:date ."""


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
