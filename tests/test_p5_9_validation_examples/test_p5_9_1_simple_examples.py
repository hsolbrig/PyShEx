import unittest

from ShExJSG import ShExJ
from rdflib import Literal

from pyshex.utils.schema_utils import reference_of
from tests.utils.setup_test import setup_test, setup_context

shex_1 = """{ "type": "Schema", "shapes": [
    { "id": "http://schema.example/IntConstraint",
      "type": "NodeConstraint",
      "datatype": "http://www.w3.org/2001/XMLSchema#integer"
    } ] }"""


class SimpleExamplesTestCase(unittest.TestCase):
    @unittest.skipIf(True, "SimpleExamplesTestCase not implemented")
    def test_example_1(self):
        # from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
        # cntxt = setup_context(shex_1, None)
        #
        # self.assertTrue(satisfies(cntxt, Literal('"30"^^<http://www.w3.org/2001/XMLSchema#integer>'),
        #     shex_1.
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
