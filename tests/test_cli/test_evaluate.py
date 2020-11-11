import os
import unittest
from typing import List

from pyshex.shex_evaluator import evaluate_cli
from tests import datadir
from tests.test_cli.clitests import CLITestCase

update_test_files: bool = False


class ShexEvaluatorTestCase(CLITestCase):
    testdir = "evaluate"
    testprog = 'shexeval'

    def prog_ep(self, argv: List[str]) -> bool:
        return evaluate_cli(argv, prog=self.testprog)

    def test_help(self):
        self.do_test("--help", 'help', update_test_file=update_test_files, failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_obs(self):
        shex = os.path.join(self.test_input_dir, 'obs.shex')
        rdf = os.path.join(self.test_input_dir, 'obs.ttl')
        self.do_test([rdf, shex, '-fn', 'http://ex.org/Obs1'], 'obs1', update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")

    def test_biolink(self):
        shex = os.path.join(datadir,'schemas', 'meta.shex')
        rdf = os.path.join(datadir, 'validation', 'biolink-model.ttl')
        self.do_test([rdf, shex, '-fn', 'https://biolink.github.io/biolink-model/ontology/biolink.ttl',
                      '-s', 'http://bioentity.io/vocab/SchemaDefinition', '-cf'], 'biolinkpass',
                     update_test_file=update_test_files)
        self.do_test([rdf, shex, '-fn', 'https://biolink.github.io/biolink-model/ontology/biolink.ttl',
                      '-s', 'http://bioentity.io/vocab/SchemaDefinition'], 'biolinkfail',
                     update_test_file=update_test_files, failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_start_type(self):
        """ Test four subjects, two having one RDF type, one having two and one having none """
        shex = os.path.join(datadir, 'schemas', 'biolink-modelnc.shex')
        rdf = os.path.join(datadir, 'validation', 'type-samples.ttl')
        self.do_test([rdf, shex, '-A', '-ut', '-cf'], 'type-samples', update_test_file=update_test_files,
                     failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_start_predicate(self):
        """ Test four subjects, two having one RDF type, one having two and one having none """
        shex = os.path.join(datadir, 'schemas', 'biolink-modelnc.shex')
        rdf = os.path.join(datadir, 'validation', 'type-samples.ttl')
        self.do_test([rdf, shex, '-A', '-sp', 'http://w3id.org/biolink/vocab/type', '-cf'], 'pred-samples',
                     update_test_file=update_test_files,
                     failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    @unittest.skipIf(True, "SPARQL query, sometimes URL is down. Need to look for an alternative.")
    def test_sparql_query(self):
        """ Test a sample DrugBank sparql query """
        shex = os.path.join(datadir, 't1.shex')
        sparql = os.path.join(datadir, 't1.sparql')
        rdf = 'http://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql'
        self.do_test([rdf, shex, '-sq', sparql], 't1', update_test_file=update_test_files)


if __name__ == '__main__':
    unittest.main()
