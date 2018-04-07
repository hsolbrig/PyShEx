import unittest

import os

from rdflib import Graph, Namespace

from pyshex import ShExEvaluator, PrefixLibrary
from pyshex.evaluate import evaluate
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

WIKIDATA = Namespace("http://www.wikidata.org/entity/")


class WikiDataTestCase(unittest.TestCase):
    test_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data',  'Q18557122.ttl')

    def test_wikidata_1(self):
        g = Graph()
        g.load(self.test_path, format="turtle")
        rslt, _ = evaluate(g, shex_schema, WIKIDATA.Q18557112)
        self.assertTrue(rslt)

    def test_wikidata_2(self):
        pfx = PrefixLibrary(shex_schema, wikidata="http://www.wikidata.org/entity/")
        evaluator = ShExEvaluator(self.test_path, shex_schema, pfx.WIKIDATA.Q18557112)
        print(evaluator.evaluate(start=pfx.GW.cancer, debug=False))


if __name__ == '__main__':
    unittest.main()
