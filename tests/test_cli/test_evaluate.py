import os
import unittest
from typing import List

from pyshex.shex_evaluator import evaluate_cli
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        shex = os.path.join(base_dir,'schemas', 'meta.shex')
        rdf = os.path.join(base_dir, 'validation', 'biolink-model.ttl')
        self.do_test([rdf, shex, '-fn', 'https://biolink.github.io/biolink-model/ontology/biolink.ttl',
                      '-s', 'http://bioentity.io/vocab/SchemaDefinition', '-cf'], 'biolinkpass',
                     update_test_file=update_test_files)
        self.do_test([rdf, shex, '-fn', 'https://biolink.github.io/biolink-model/ontology/biolink.ttl',
                      '-s', 'http://bioentity.io/vocab/SchemaDefinition'], 'biolinkfail',
                     update_test_file=update_test_files, failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_start_type(self):
        """ This tests four subjects, two having one RDF type, one having two and one having none """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        shex = os.path.join(base_dir, 'schemas', 'biolink-modelnc.shex')
        rdf = os.path.join(base_dir, 'validation', 'type-samples.ttl')
        self.do_test([rdf, shex, '-A', '-ut', '-cf'], 'type-samples', update_test_file=update_test_files,
                     failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")

    def test_start_predicate(self):
        """ This tests four subjects, two having one RDF type, one having two and one having none """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        shex = os.path.join(base_dir, 'schemas', 'biolink-modelnc.shex')
        rdf = os.path.join(base_dir, 'validation', 'type-samples.ttl')
        self.do_test([rdf, shex, '-A', '-sp', 'http://w3id.org/biolink/vocab/type', '-cf'], 'pred-samples',
                     update_test_file=update_test_files,
                     failexpected=True)
        self.assertFalse(update_test_files, "Updating test files")


if __name__ == '__main__':
    unittest.main()
