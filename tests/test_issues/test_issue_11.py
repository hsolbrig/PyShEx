import os
import unittest

from rdflib import Namespace

from pyshex import ShExEvaluator

WIKIDATA = Namespace("http://www.wikidata.org/entity/")


class FalsePositiveTestCase(unittest.TestCase):
    test_data = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')

    def test_false_positive_minimum(self):
        with open(os.path.join(self.test_data, 'disease_min.shex')) as f:
            shex = f.read()
        e = ShExEvaluator(os.path.join(self.test_data, 'Q12214_min.ttl'), shex, WIKIDATA.Q12214, debug=False)
        self.assertFalse(e.evaluate()[0].result)

    def test_false_positive_minimum_2(self):
        with open(os.path.join(self.test_data, 'disease_min.shex')) as f:
            shex = f.read()
        e = ShExEvaluator(os.path.join(self.test_data, 'Q12214_min_2.ttl'), shex, WIKIDATA.Q12214, debug=False)
        self.assertFalse(e.evaluate()[0].result)

    def test_false_positive(self):
        with open(os.path.join(self.test_data, 'shex', 'disease.shex')) as f:
            shex = f.read()
        e = ShExEvaluator(os.path.join(self.test_data, 'Q12214.ttl'), shex, WIKIDATA.Q12214, debug=False)
        self.assertFalse(e.evaluate()[0].result)


if __name__ == '__main__':
    unittest.main()
