import unittest

from pyshex import ShExEvaluator, PrefixLibrary

shex = """
BASE <http://example.org/ex/>
PREFIX ex: <http://example.org/ex/>


start = @<S>

<S> { ex:p . }
"""

rdf = """
BASE <http://example.org/ex/>

<s> <p> "Stuff" .
"""


class Issue23TestCase(unittest.TestCase):
    def test_fail(self):
        pl = PrefixLibrary(shex)
        results = ShExEvaluator().evaluate(rdf, shex, focus=pl.EX.s, debug=False)
        self.assertTrue(results[0].result)
        results = ShExEvaluator().evaluate(rdf, shex, focus=pl.EX.t)
        self.assertFalse(results[0].result)
        self.assertEqual('Focus: http://example.org/ex/t not in graph', results[0].reason)
        results2 = ShExEvaluator().evaluate(rdf, shex, focus=[pl.EX.s, pl.EX.t2])
        self.assertTrue(results2[0].result)
        self.assertFalse(results2[1].result)
        self.assertEqual('Focus: http://example.org/ex/t2 not in graph', results2[1].reason)


if __name__ == '__main__':
    unittest.main()
