import unittest

from rdflib import Graph, Literal

rdf = '<x> <y> "ab"^^<http://a.example/bloodType>.'


class DTTestCase(unittest.TestCase):
    def test_wild_datatype(self):
        """ Make sure that non-standard datatypes are preserved in rdflib"""
        g = Graph()
        ts = g.parse(data=rdf, format="turtle")
        self.assertEqual(list(ts.objects())[0], Literal('ab', datatype='http://a.example/bloodType'))


if __name__ == '__main__':
    unittest.main()
