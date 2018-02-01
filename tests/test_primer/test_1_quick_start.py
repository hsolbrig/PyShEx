import unittest

from rdflib import Graph, Namespace

from pyshex.evaluate import evaluate

shexc = """PREFIX school: <http://school.example/#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://ex.example/#>

# Node constraint
school:enrolleeAge xsd:integer MinInclusive 13 MaxInclusive 20


school:Enrollee {
  # Triple constraint (including node constraint IRI)
  ex:hasGuardian IRI {1,2}
}
"""

rdf1 = """PREFIX ex: <http://ex.example/#>
PREFIX inst: <http://example.com/users/>

inst:Student1 ex:hasGuardian
  inst:Person2, inst:Person3 ."""

EX = Namespace("http://ex.example/#")
SCHOOL = Namespace("http://school.example/#")


class QuickStartTestCase(unittest.TestCase):
    @unittest.skipIf(True, "Not yet implemented")
    def test_first_example(self):
        g = Graph()
        g.parse(data=rdf1, format="turtle")
        rslt, reason = evaluate(g, shexc, EX.obs1, SCHOOL.Enrollee)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
