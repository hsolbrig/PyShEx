import os
import sys
import unittest

from pyshex import ShExEvaluator
from CFGraph import CFGraph


class ShexEvalTestCase(unittest.TestCase):

    def test_biolink_shexeval(self) -> None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        g = CFGraph()
        g.load(os.path.join(base_dir, 'validation', 'biolink-model.ttl'), format="turtle")
        evaluator = ShExEvaluator(g,
                                  os.path.join(base_dir, 'schemas', 'meta.shex'),
                                  "https://biolink.github.io/biolink-model/ontology/biolink.ttl",
                                  "http://bioentity.io/vocab/SchemaDefinition")
        result = evaluator.evaluate(debug=False)
        for rslt in result:
            if not rslt.result:
                print(f"Error: {rslt.reason}")
        self.assertTrue(all(r.result for r in result))



if __name__ == '__main__':
    unittest.main()
