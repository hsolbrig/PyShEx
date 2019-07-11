import os
import unittest

from rdflib import Namespace

from pyshex import ShExEvaluator

BASE = Namespace("https://w3id.org/biolink/vocab/")

rdf = f"""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX SEMMEDDB: <http://example.org/UNKNOWN/SEMMEDDB/>
PREFIX WD: <http://example.org/UNKNOWN/WD/>

<http://identifiers.org/drugbank:DB00005> a WD:Q12140;
  rdfs:subClassOf <http://identifiers.org/mesh/D000602>;
  dcterms:description "Dimeric fusion protein consisting of ...";
  rdfs:label "Etanercept";
  <https://w3id.org/biolink/vocab/systematic_synonym> "BIOD00052" .
"""


class Issue51TestCase(unittest.TestCase):
    test_data = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')

    def test_performance_problem(self):
        """ Test a performance problem brought about by two possible type arcs in a definition """

        e = ShExEvaluator(rdf=rdf, schema=os.path.join(self.test_data, 'shex', 'issue_54.shex'),
                          focus="http://identifiers.org/drugbank:DB00005",
                          start="https://w3id.org/biolink/vocab/Drug").evaluate()
        self.assertTrue(e[0].result)


if __name__ == '__main__':
    unittest.main()
