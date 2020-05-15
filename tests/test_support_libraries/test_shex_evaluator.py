import os
from rdflib import Graph, URIRef

from pyshex import ShExEvaluator, PrefixLibrary
import unittest

from pyshex.shapemap_structure_and_language.p3_shapemap_structure import START

shex_schema = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX prv: <http://www.wikidata.org/prop/reference/value/>
PREFIX pv: <http://www.wikidata.org/prop/value/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX gw: <http://genewiki.shape/>


start = @gw:cancer
gw:cancer {
  p:P1748 {
    prov:wasDerivedFrom @<reference>
  }+
}

<reference> {
  pr:P248  IRI ;
  pr:P813  xsd:dateTime ;
  pr:P699  LITERAL
}
"""

loc_prefixes = PrefixLibrary(None,
                             wikidata="http://www.wikidata.org/entity/",
                             gw="http://genewiki.shape/")


class ShExEvaluatorTestCase(unittest.TestCase):
    def test_empty_constructor(self):
        evaluator = ShExEvaluator()
        # rdflib no longer emits unused prefixes -- an empty evaluator is now empty
        self.assertEqual("", evaluator.rdf.strip())
        self.assertIsNone(evaluator.schema)
        self.assertIsNone(evaluator.focus)
        self.assertEqual([], evaluator.foci)
        self.assertEqual([START], evaluator.start)
        self.assertEqual("turtle", evaluator.rdf_format)
        self.assertTrue(isinstance(evaluator.g, Graph))

    def test_complete_constructor(self):
        test_rdf = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'test_issues', 'data', 'Q18557122.ttl')
        evaluator = ShExEvaluator(test_rdf, shex_schema,
                                  [loc_prefixes.WIKIDATA, loc_prefixes.WIKIDATA.Q18557112],
                                  loc_prefixes.WIKIDATA.cancer)
        results = evaluator.evaluate()
        self.assertFalse(results[0].result)
        self.assertEqual(URIRef('http://www.wikidata.org/entity/'), results[0].focus)
        self.assertEqual(URIRef('http://www.wikidata.org/entity/cancer'), results[0].start)
        self.assertEqual('Focus: http://www.wikidata.org/entity/ not in graph', results[0].reason)
        self.assertEqual(URIRef('http://www.wikidata.org/entity/Q18557112'), results[1].focus)
        self.assertEqual(URIRef('http://www.wikidata.org/entity/cancer'), results[1].start)
        self.assertEqual('  Shape: http://www.wikidata.org/entity/cancer not found in Schema',
                         results[1].reason)


if __name__ == '__main__':
    unittest.main()
