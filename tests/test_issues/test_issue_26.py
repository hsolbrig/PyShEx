import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from pyshex.shex_evaluator import evaluate_cli

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
validation_dir = os.path.join(data_dir, 'validation')
rdffile = os.path.join(validation_dir, 'anon_start.ttl')
shexfile = os.path.join(validation_dir, 'anon_start.shex')


class Issue26TestCase(unittest.TestCase):

    @unittest.skipIf(False, "Issue 26 needs to be fixed")
    def test_anon_start(self):
        self.assertEqual(0, evaluate_cli(f"{rdffile} {shexfile} -A"))



if __name__ == '__main__':
    unittest.main()
