import unittest

from rdflib import Namespace, XSD
from pyshex import ShExEvaluator

EX = Namespace("http://example.org/")

shex = f"""PREFIX : <{EX}> 
PREFIX xsd: <{XSD}>

start = @<A>

<A> {{:p1 xsd:string }}
"""

data = f"""PREFIX : <{EX}>

:d :p1 "final" .
"""


class ShexjsIssue17TestCase(unittest.TestCase):
    # Test of https://github.com/shexSpec/shex.js/issues/17

    def test_infinite_loop(self):
        e = ShExEvaluator(rdf=data, schema=shex, focus=EX.d)
        rslt = e.evaluate(debug=False)
        self.assertTrue(rslt[0].result)


if __name__ == '__main__':
    unittest.main()
