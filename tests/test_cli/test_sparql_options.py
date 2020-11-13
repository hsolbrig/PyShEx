import os
import re
import unittest
from typing import List

from pyshex.shex_evaluator import evaluate_cli
from tests import datadir
from tests.test_cli.clitests import CLITestCase


def elapsed_filter(txt: str) -> str:
    return re.sub(r'\(\d+(\.\d+)? ([a-zA-Z]*)\)', '(n.nn \\2)', txt)


class SparqlQueryTestCase(CLITestCase):
    testdir = "evaluate"
    testprog = 'shexeval'
    schemadir = os.path.join(datadir, 'schemas')

    def prog_ep(self, argv: List[str]) -> bool:
        return bool(evaluate_cli(argv, prog=self.testprog))

    @unittest.skipIf(True, "SPARQL query, sometimes URL is down. Need to look for an alternative.")
    def test_sparql_query(self):
        """ Test a sample DrugBank sparql query """
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        rdf = 'http://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql'
        self.do_test([rdf, shex, '-sq', sparql], 'dbsparql1')

    @unittest.skipIf(True, "SPARQL query, sometimes URL is down. Need to look for an alternative.")
    def test_print_queries(self):
        """ Test a sample DrugBank sparql query printing queries"""
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        rdf = 'http://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql'
        self.do_test([rdf, shex, '-sq', sparql, '-ps'], 'dbsparql2', text_filter=elapsed_filter)

    @unittest.skipIf(True, "SPARQL query, sometimes URL is down. Need to look for an alternative.")
    def test_print_results(self):
        """ Test a sample DrugBank sparql query printing results"""
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        rdf = 'http://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql'
        self.do_test([rdf, shex, '-sq', sparql, '-pr', "--stopafter", "1"], 'dbsparql3', text_filter=elapsed_filter)

    @unittest.skipIf(True, "SPARQL query, sometimes URL is down. Need to look for an alternative.")
    def test_named_graph(self):
        """ Test a sample DrugBank using any named graph """

        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        rdf = 'http://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql'
        self.maxDiff = None
        self.do_test([rdf, shex, '-sq', sparql, '-ps', '-gn', "", "-pr"], 'dbsparql4', failexpected=True,
                     text_filter=elapsed_filter)

        graphid = "<http://identifiers.org/drugbank:>"
        self.do_test([rdf, shex, '-sq', sparql, '-ps', '-gn', graphid, "-pr"], 'dbsparql5', failexpected=True,
                     text_filter=elapsed_filter)

    @unittest.skipIf(True, "Volatile query - run this to make sure it works, but don't compare output")
    def test_named_graph_types(self):
        """ Test a Drugbank query with named graph in the query """
        shex = os.path.join(datadir, 'schemas', 'biolink-modelnc.shex')
        rdf = 'http://graphdb.dumontierlab.com/repositories/ncats-red-kg'
        self.maxDiff = None
        self.do_test([rdf, shex, '-ss', '-gn', '', '-ps', '-pr', '-ut', '-sq',
                      'select ?item where{?item a <http://w3id.org/biolink/vocab/Protein>} LIMIT 20'],
                     'dbsparql6', failexpected=True, text_filter=elapsed_filter)

    @unittest.skipIf(True, "pat4 can (and is) in the DB multiple times -- this is a FHIR problem")
    def test_infer_setting(self):
        """ Test setting infer to False """

        shex = os.path.join(datadir, 'patient.shex')
        rdf = 'https://graph.fhircat.org/repositories/fhirontology?infer=false'
        self.maxDiff = None
        self.do_test([rdf, shex, '-fn', "http://hl7.org/fhir/Patient/pat4", '-ssg', '-pb', '-ps', '-pr'], 'dbsparql7',
                     text_filter=elapsed_filter)


if __name__ == '__main__':
    unittest.main()
