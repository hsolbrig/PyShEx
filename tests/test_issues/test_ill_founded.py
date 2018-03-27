import unittest

from rdflib import Graph, Namespace

from pyshex import ShExEvaluator

shex = """<http://a.example/S> {<http://a.example/p> not @<http://a.example/S>}"""
EX = Namespace("http://a.example/")


class IllFoundedTestCase(unittest.TestCase):

    def test_false_positive_minimum(self):
        g = Graph()
        g.add((EX.x, EX.p, EX.x))
        e = ShExEvaluator(rdf=g, schema=shex, focus=EX.x, start=EX.S, debug=True)
        g = Graph()
        self.assertTrue(e.evaluate()[0].result)
        g.add((EX.y, EX.p, EX.z))
        self.assertFalse(e.evaluate()[0].result)


if __name__ == '__main__':
    unittest.main()
