import unittest

from pyshexc.parser_impl.generate_shexj import parse

shex_schema = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX prv: <http://www.wikidata.org/prop/reference/value/>
PREFIX pv: <http://www.wikidata.org/prop/value/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX gw: <http://genewiki.shape/>


start = @gw:cancer  # comment
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


class ShexCommentTestCase(unittest.TestCase):

    def test_1(self):
        parse(shex_schema)
        self.assertTrue(True, "Parser didn't die")


if __name__ == '__main__':
    unittest.main()
