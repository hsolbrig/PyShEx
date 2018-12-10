import unittest

from rdflib import Graph, Namespace

from pyshex import ShExEvaluator

shex = """<http://a.example/S> {<http://a.example/p> not @<http://a.example/S>}"""
EX = Namespace("http://a.example/")


class NoStartNodeTestCase(unittest.TestCase):

    def test_no_start(self):
        g = Graph()
        g.add((EX.x, EX.p, EX.x))
        e = ShExEvaluator(rdf=g, schema=shex, focus=EX.x)
        rslt = e.evaluate()[0]
        self.assertFalse(rslt.result)
        self.assertEqual('START node is not specified', rslt.reason.strip())

    def test_bad_start(self):
        g = Graph()
        g.add((EX.x, EX.p, EX.x))
        e = ShExEvaluator(rdf=g, schema=shex, start=EX.c, focus=EX.x)
        rslt = e.evaluate()[0]
        self.assertFalse(rslt.result)
        self.assertEqual('Shape: http://a.example/c not found in Schema', rslt.reason.strip())


if __name__ == '__main__':
    unittest.main()
