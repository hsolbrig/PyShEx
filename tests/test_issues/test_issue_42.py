import unittest

from pyshex import ShExEvaluator, PrefixLibrary

shex = """
PREFIX ex: <http://example.org/ex/>
START = @<S>

<S> { ex:p . }
"""

rdf = """
BASE <http://example.org/ex/>

<s> <p> "Stuff" .
<a> <t> "Other stuff" .
"""

NUM_ITERS = 3

class Issue42TestCase(unittest.TestCase):
    def test_multiple_evaluate(self):
        """ Test calling evaluate multiple times in a row """
        p = PrefixLibrary(shex)
        e = ShExEvaluator(rdf=rdf, schema=shex, focus=p.EX.s)

        # conformant
        for _ in range(NUM_ITERS):
            self.assertTrue(e.evaluate()[0].result)

        # non-conformant
        for _ in range(NUM_ITERS):
            self.assertFalse(e.evaluate(focus=p.EX.a)[0].result)

if __name__ == '__main__':
    unittest.main()
