import unittest
from pprint import pprint

from pyshex import ShExEvaluator

shex = """
prefix : <http://examples.org/ex/>

start = @<S3>

<S1> {$<S1TP> (:ex1a .; :ex1b .)}
<S2> {$<S2TP> (:ex2a .; :ex2b .)}
<S3> CLOSED {&<S1TP>; &<S2TP>;}
"""

passing = """
prefix : <http://examples.org/ex/>

:t :ex1a 1; :ex1b 2; :ex2a 3; :ex2b 4 .
"""

failing_1 = """
prefix : <http://examples.org/ex/>

:t :ex1a 1; :ex1b 2; :ex2a 3 .
"""

failing_2 = """
prefix : <http://examples.org/ex/>

:t :ex1a 1; :ex1b 2; :ex2a 3; :ex2b 4; a :foo.
"""


class TeLabelTestCase(unittest.TestCase):
    def test_te_labels(self):
        """ Test triple expression labels """
        e = ShExEvaluator(rdf=passing, schema=shex, focus="http://examples.org/ex/t").evaluate(debug=False)
        pprint(e)
        self.assertTrue(e[0].result)

        e = ShExEvaluator(rdf=failing_1, schema=shex, focus="http://examples.org/ex/t").evaluate()
        self.assertFalse(e[0].result)

        e = ShExEvaluator(rdf=failing_2, schema=shex, focus="http://examples.org/ex/t").evaluate()
        self.assertFalse(e[0].result)


if __name__ == '__main__':
    unittest.main()
