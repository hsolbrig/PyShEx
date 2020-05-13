import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from rdflib import Graph, Namespace, URIRef

from pyshex import PrefixLibrary, standard_prefixes, known_prefixes

# Install the turtle w/ prefixes library
from pyshex.utils import tortoise

tortoise.register()


class PrefixLibTestCase(unittest.TestCase):
    def test_basics(self):
        """ Test basic functions """
        pl = PrefixLibrary()
        print(str(pl))
        g = Graph()
        pl.add_bindings_to(g)

        # Version 5.0.0 of rdflib no longer emits unused prefixes, so we use the "tortoise" extension
        self.assertEqual("""@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""", g.serialize(format="tortoise").decode().strip())
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

        known_prefixes.add_bindings_to(g)
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
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""", g.serialize(format="tortoise").decode().strip())

    def test_nsname(self):
        """ Test the nsname method """
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

    def test_add_to_object(self):
        """ Test the PrefixLibrary add_to_object function """
        class TargetObj:
            pass

        pl = PrefixLibrary("""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX pr: <http://www.wikidata.org/prop/reference/>
        PREFIX prv: <http://www.wikidata.org/prop/reference/value/>
        PREFIX pv: <http://www.wikidata.org/prop/value/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX gw: <http://genewiki.shape/>""")
        self.assertEqual(8, pl.add_to_object(TargetObj))
        self.assertEqual(URIRef('http://www.w3.org/ns/prov#spiders'), TargetObj.PROV.spiders)

        class TargetObj2:
            GW: int = 42
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(7, pl.add_to_object(TargetObj2))
        self.assertTrue(output.getvalue().strip().startswith("Warning: GW is already defined in namespace "))

    def test_add_to_module(self):
        """ Test the ability to inject namespaces into the surrounding module """
        output = StringIO()
        with redirect_stdout(output):
            from tests.test_support_libraries import local_context

        self.assertTrue(output.getvalue().startswith('Warning: XSD is already defined in namespace'))
        self.assertEqual(URIRef("http://www.w3.org/ns/prov#drooling"), local_context.sample('drooling'))
        self.assertEqual(URIRef("http://nonxml.com/item#type"), local_context.rdf('type'))

    def test_add_shex_filename(self):
        """ Test adding Shex from a file """
        filename = os.path.join(os.path.dirname(__file__), '..', 'data', 't1.shex')
        pl = PrefixLibrary(filename)
        self.assertEqual("""PREFIX drugbank: <http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugbank/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>""", str(pl).strip())
        self.assertEqual(URIRef("http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugbank/junk"),
                         pl.DRUGBANK.junk)

    def test_add_shex_url(self):
        """ Test adding ShEx from a URL """
        pl = PrefixLibrary(
            "https://raw.githubusercontent.com/SuLab/Genewiki-ShEx/master/diseases/wikidata-disease-ontology.shex")
        self.assertEqual("""PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX prv: <http://www.wikidata.org/prop/reference/value/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX do: <http://purl.obolibrary.org/obo/DOID_>
PREFIX doio: <http://identifiers.org/doid/>
PREFIX mir: <http://www.ebi.ac.uk/miriam/main/collections/>""", str(pl).strip())


    def test_add_rdf_str(self):
        """ Test adding RDF directly from a string """
        pl = PrefixLibrary()

        rdf = """
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ex: <http://example.org/test/> .

ex:Sam a foaf:Person."""
        pl.add_rdf(rdf)
        self.assertEqual("""PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/test/>""", str(pl).strip())

    def test_add_rdf_file(self):
        """ Test adding RDF directly from a file """
        # Note: earlier versions of this included an 'PREFIX ex: <http://example.org/>' -- the latest doesn't
        filename = os.path.join(os.path.dirname(__file__), '..', 'data', 'earl_report.ttl')
        pl = PrefixLibrary()
        self.assertEqual("""PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX earl: <http://www.w3.org/ns/earl#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ns1: <http://purl.org/dc/elements/1.1/>""", str(pl.add_rdf(filename)).strip())
        g = Graph()
        g.load(filename, format="turtle")
        pl = PrefixLibrary()
        self.assertEqual("""PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX earl: <http://www.w3.org/ns/earl#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ns1: <http://purl.org/dc/elements/1.1/>""", str(pl.add_rdf(g)).strip())

    def test_add_rdf_url(self):
        """ Test adding RDF from a URL """
        pl = PrefixLibrary()
        pl.add_rdf("https://raw.githubusercontent.com/prefixcommons/biocontext/master/registry/go_context.jsonld",
                   format="json-ld")
        self.assertEqual("""PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wb: <http://identifiers.org/wormbase/>
PREFIX kegg_ligand: <http://www.genome.jp/dbget-bin/www_bget?cpd:>
PREFIX pso_git: <https://github.com/Planteome/plant-stress-ontology/issues/>
PREFIX ncbigene: <http://identifiers.org/ncbigene/>
PREFIX kegg_reaction: <http://www.genome.jp/dbget-bin/www_bget?rn:>
PREFIX go_ref: <http://purl.obolibrary.org/obo/go/references/>
PREFIX vega: <http://vega.sanger.ac.uk/id/>
PREFIX zfin: <http://identifiers.org/zfin/>
PREFIX pfam: <http://pfam.xfam.org/family/>
PREFIX sgn: <http://identifiers.org/sgn/>
PREFIX reactome: <http://identifiers.org/reactome/>
PREFIX interpro: <http://identifiers.org/interpro/>
PREFIX unirule: <http://www.uniprot.org/unirule/>
PREFIX dictybase: <http://identifiers.org/dictybase.gene/>
PREFIX po_git: <https://github.com/Planteome/plant-ontology/issues/>
PREFIX aspgd_locus: <http://identifiers.org/aspgd.locus/>
PREFIX sgd: <http://identifiers.org/sgd/>
PREFIX hgnc: <http://identifiers.org/hgnc/>
PREFIX dictybase_gene_name: <http://dictybase.org/gene/>
PREFIX tair: <http://identifiers.org/tair.locus/>
PREFIX ensemblfungi: <http://www.ensemblgenomes.org/id/>
PREFIX wikipedia: <http://en.wikipedia.org/wiki/>
PREFIX psi-mod: <http://www.ebi.ac.uk/ontology-lookup/?termId=MOD:>
PREFIX rgd: <http://identifiers.org/rgd/>
PREFIX pmid: <http://www.ncbi.nlm.nih.gov/pubmed/>
PREFIX xenbase: <http://identifiers.org/xenbase/>
PREFIX maizegdb: <http://maizegdb.org/gene_center/gene/>
PREFIX hamap: <http://hamap.expasy.org/unirule/>
PREFIX to_git: <https://github.com/Planteome/plant-trait-ontology/issues/>
PREFIX mesh: <http://n2t.net/MESH:>
PREFIX gr_protein: <http://identifiers.org/gramene.protein/>
PREFIX pombase: <http://identifiers.org/pombase/>
PREFIX ena: <http://www.ebi.ac.uk/ena/data/view/>
PREFIX ec: <http://www.expasy.org/enzyme/>
PREFIX uniprotkb: <http://identifiers.org/uniprot/>
PREFIX mgi: <http://identifiers.org/mgi/>
PREFIX gomodel: <http://model.geneontology.org/>
PREFIX kegg_pathway: <http://identifiers.org/kegg.pathway/>
PREFIX doi: <http://dx.doi.org/>
PREFIX panther: <http://identifiers.org/panther.family/>
PREFIX fb: <http://identifiers.org/flybase/>
PREFIX ensembl: <http://identifiers.org/ensembl/>
PREFIX cgd: <http://identifiers.org/cgd/>
PREFIX gr_gene: <http://identifiers.org/gramene.gene/>
PREFIX kegg_enzyme: <http://identifiers.org/kegg.enzyme/>
PREFIX cacao: <http://gowiki.tamu.edu/wiki/index.php/>
PREFIX po_ref: <http://planteome.org/po_ref/>
PREFIX uniprotkb-subcell: <http://www.uniprot.org/locations/>
PREFIX nif_subcellular: <http://www.neurolex.org/wiki/>
PREFIX genedb: <http://identifiers.org/genedb/>
PREFIX apidb_plasmodb: <http://www.plasmodb.org/gene/>
PREFIX rnacentral: <http://rnacentral.org/rna/>
PREFIX rfam: <http://rfam.sanger.ac.uk/family/>
PREFIX obo_sf2_po: <http://sourceforge.net/p/obo/plant-ontology-po-term-requests/>
PREFIX uniparc: <http://www.uniprot.org/uniparc/>
PREFIX gdb: <http://www.gdb.org/gdb-bin/genera/accno?accessionNum=GDB:>
PREFIX dbsnp: <http://identifiers.org/dbsnp/>
PREFIX maizegdb_locus: <http://identifiers.org/maizegdb.locus/>
PREFIX mo: <http://mged.sourceforge.net/ontologies/MGEDontology.php#>
PREFIX plana_ref: <http://purl.obolibrary.org/obo/plana/references/>
PREFIX cas: <http://identifiers.org/cas/>
PREFIX complexportal: <https://www.ebi.ac.uk/complexportal/complex/>
PREFIX jstor: <http://www.jstor.org/stable/>
PREFIX gr_qtl: <http://identifiers.org/gramene.qtl/>
PREFIX vbrc: <http://vbrc.org/query.asp?web_id=VBRC:>
PREFIX eo_git: <https://github.com/Planteome/plant-environment-ontology/issues/>
PREFIX tgd: <http://identifiers.org/tgd/>
PREFIX obo_sf2_peco: <https://sourceforge.net/p/obo/plant-environment-ontology-eo/>
PREFIX metacyc: <http://identifiers.org/metacyc/>
PREFIX omim: <http://omim.org/entry/>
PREFIX intact: <http://identifiers.org/intact/>
PREFIX ensembl_geneid: <http://www.ensembl.org/id/>
PREFIX uniprotkb-kw: <http://www.uniprot.org/keywords/>
PREFIX eupathdb: <http://eupathdb.org/gene/>""", str(pl).strip())

    def test_standardprefixes(self):
        """ Test the pre-packaged standard prefixes """
        self.assertEqual("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>""", str(standard_prefixes).strip())

    def test_knownprefixes(self):
        """ Test the pre-packaged known prefixes """
        self.assertEqual("""PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX xmlns: <http://www.w3.org/XML/1998/namespace>""", str(known_prefixes).strip())

    def test_edge_cases(self):
        """ Test some of the edge cases """
        # Test a default URL
        shex = "PREFIX : <http://example.org/sample/>"
        pl = PrefixLibrary(shex)
        print(str(pl).strip())


if __name__ == '__main__':
    unittest.main()
