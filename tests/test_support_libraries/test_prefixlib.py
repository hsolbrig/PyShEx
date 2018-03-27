import unittest

from rdflib import Graph, Namespace

from pyshex import PrefixLibrary, standard_prefixes, known_prefixes


class PrefixLibTestCase(unittest.TestCase):
    def test_1(self):
        pl = PrefixLibrary()
        print(str(pl))
        g = Graph()
        pl.add_bindings(g)

        self.assertEqual("""@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""", g.serialize(format="turtle").decode().strip())
        pl = PrefixLibrary("""@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix wikibase: <http://wikiba.se/ontology-beta#> .
@prefix wds: <http://www.wikidata.org/entity/statement/> .
@prefix wdata: <https://www.wikidata.org/wiki/Special:EntityData/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix schema: <http://schema.org/> .
@prefix cc: <http://creativecommons.org/ns#> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix wdref: <http://www.wikidata.org/reference/> .
@prefix wdv: <http://www.wikidata.org/value/> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix wdt: <http://www.wikidata.org/prop/direct/> .
@prefix wdtn: <http://www.wikidata.org/prop/direct-normalized/> .
@prefix p: <http://www.wikidata.org/prop/> .
@prefix ps: <http://www.wikidata.org/prop/statement/> .
@prefix psv: <http://www.wikidata.org/prop/statement/value/> .
@prefix psn: <http://www.wikidata.org/prop/statement/value-normalized/> .
@prefix pq: <http://www.wikidata.org/prop/qualifier/> .
@prefix pqv: <http://www.wikidata.org/prop/qualifier/value/> .
@prefix pqn: <http://www.wikidata.org/prop/qualifier/value-normalized/> .
@prefix pr: <http://www.wikidata.org/prop/reference/> .
@prefix prv: <http://www.wikidata.org/prop/reference/value/> .
@prefix prn: <http://www.wikidata.org/prop/reference/value-normalized/> .
@prefix wdno: <http://www.wikidata.org/prop/novalue/> .

and some junk""")

        self.assertEqual(
            [('OWL', Namespace('http://www.w3.org/2002/07/owl#')),
             ('WIKIBASE', Namespace('http://wikiba.se/ontology-beta#')),
             ('WDS', Namespace('http://www.wikidata.org/entity/statement/')),
             ('WDATA', Namespace('https://www.wikidata.org/wiki/Special:EntityData/')),
             ('SKOS', Namespace('http://www.w3.org/2004/02/skos/core#')),
             ('SCHEMA', Namespace('http://schema.org/')),
             ('CC', Namespace('http://creativecommons.org/ns#')),
             ('GEO', Namespace('http://www.opengis.net/ont/geosparql#')),
             ('PROV', Namespace('http://www.w3.org/ns/prov#')),
             ('WDREF', Namespace('http://www.wikidata.org/reference/')),
             ('WDV', Namespace('http://www.wikidata.org/value/')),
             ('WD', Namespace('http://www.wikidata.org/entity/')),
             ('WDT', Namespace('http://www.wikidata.org/prop/direct/')),
             ('WDTN', Namespace('http://www.wikidata.org/prop/direct-normalized/')),
             ('P', Namespace('http://www.wikidata.org/prop/')),
             ('PS', Namespace('http://www.wikidata.org/prop/statement/')),
             ('PSV', Namespace('http://www.wikidata.org/prop/statement/value/')),
             ('PSN', Namespace('http://www.wikidata.org/prop/statement/value-normalized/')),
             ('PQ', Namespace('http://www.wikidata.org/prop/qualifier/')),
             ('PQV', Namespace('http://www.wikidata.org/prop/qualifier/value/')),
             ('PQN', Namespace('http://www.wikidata.org/prop/qualifier/value-normalized/')),
             ('PR', Namespace('http://www.wikidata.org/prop/reference/')),
             ('PRV', Namespace('http://www.wikidata.org/prop/reference/value/')),
             ('PRN', Namespace('http://www.wikidata.org/prop/reference/value-normalized/')),
             ('WDNO', Namespace('http://www.wikidata.org/prop/novalue/'))], [e for e in pl]
        )
        
        pl = PrefixLibrary("""
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
}""", foaf=known_prefixes.FOAF, owl=known_prefixes.OWL, rdfs=standard_prefixes.RDFS)
        self.assertEqual(
            [('XSD', Namespace('http://www.w3.org/2001/XMLSchema#')),
             ('PROV', Namespace('http://www.w3.org/ns/prov#')),
             ('P', Namespace('http://www.wikidata.org/prop/')),
             ('PR', Namespace('http://www.wikidata.org/prop/reference/')),
             ('PRV', Namespace('http://www.wikidata.org/prop/reference/value/')),
             ('PV', Namespace('http://www.wikidata.org/prop/value/')),
             ('PS', Namespace('http://www.wikidata.org/prop/statement/')),
             ('GW', Namespace('http://genewiki.shape/')),
             ('FOAF', Namespace('http://xmlns.com/foaf/0.1/')),
             ('OWL', Namespace('http://www.w3.org/2002/07/owl#')),
             ('RDFS', Namespace('http://www.w3.org/2000/01/rdf-schema#'))], [e for e in pl])

        pl = PrefixLibrary(None, ex="http://example.org/")
        self.assertEqual("http://example.org/", str(pl.EX))

        known_prefixes.add_bindings(g)
        self.assertEqual("""@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xmlns: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""", g.serialize(format="turtle").decode().strip())

    def test_nsname(self):
        pl = PrefixLibrary("""@prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix wikibase: <http://wikiba.se/ontology-beta#> .
        @prefix wds: <http://www.wikidata.org/entity/statement/> .
        @prefix wdata: <https://www.wikidata.org/wiki/Special:EntityData/> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix schema: <http://schema.org/> .
        @prefix cc: <http://creativecommons.org/ns#> .
        @prefix geo: <http://www.opengis.net/ont/geosparql#> .
        @prefix prov: <http://www.w3.org/ns/prov#> .
        @prefix wdref: <http://www.wikidata.org/reference/> .
        @prefix wdv: <http://www.wikidata.org/value/> .
        @prefix wd: <http://www.wikidata.org/entity/> .
        @prefix wdt: <http://www.wikidata.org/prop/direct/> .
        @prefix wdtn: <http://www.wikidata.org/prop/direct-normalized/> .
        @prefix p: <http://www.wikidata.org/prop/> .
        @prefix ps: <http://www.wikidata.org/prop/statement/> .
        @prefix psv: <http://www.wikidata.org/prop/statement/value/> .
        @prefix psn: <http://www.wikidata.org/prop/statement/value-normalized/> .
        @prefix pq: <http://www.wikidata.org/prop/qualifier/> .
        @prefix pqv: <http://www.wikidata.org/prop/qualifier/value/> .
        @prefix pqn: <http://www.wikidata.org/prop/qualifier/value-normalized/> .
        @prefix pr: <http://www.wikidata.org/prop/reference/> .
        @prefix prv: <http://www.wikidata.org/prop/reference/value/> .
        @prefix prn: <http://www.wikidata.org/prop/reference/value-normalized/> .
        @prefix wdno: <http://www.wikidata.org/prop/novalue/> .

        and some junk""")
        self.assertEqual("wdt:penguins", pl.nsname("http://www.wikidata.org/prop/direct/penguins"))
        self.assertEqual("p:polarbear", pl.nsname("http://www.wikidata.org/prop/polarbear"))
        self.assertEqual("psn:elf", pl.nsname("http://www.wikidata.org/prop/statement/value-normalized/elf"))
        self.assertEqual("http://www.wikidata1.org/prop/qualifier/",
                         pl.nsname("http://www.wikidata1.org/prop/qualifier/"))



if __name__ == '__main__':
    unittest.main()
