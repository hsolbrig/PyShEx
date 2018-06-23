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
        self.do_test("--help", 'help', update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")

    def test_obs(self):
        shex = os.path.join(self.test_input_dir, 'obs.shex')
        rdf = os.path.join(self.test_input_dir, 'obs.ttl')
        self.do_test([rdf, shex, '-fn', 'http://ex.org/Obs1'], 'obs1', update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")


if __name__ == '__main__':
    unittest.main()
