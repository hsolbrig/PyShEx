import os
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

from pyshex.shex_evaluator import evaluate_cli

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
validation_dir = os.path.join(data_dir, 'validation')
rdffile = os.path.join(validation_dir, 'simple.ttl')
shexfile = os.path.join(validation_dir, 'simple.shex')


class Issue25TestCase(unittest.TestCase):

    def test_nostart(self):
        outf = StringIO()
        with(redirect_stdout(outf)):
            evaluate_cli(f"{rdffile} {shexfile} -A".split())
        self.assertEqual("""Errors:
  Focus: None
  Start: None
  Reason: START node is not specified""", outf.getvalue().strip())

    def test_all_nodes(self):
        outf = StringIO()
        with(redirect_stderr(outf)):
            evaluate_cli(f"{rdffile} {shexfile} -s http://example.org/shapes/S".split())
        self.assertEqual('Error: You must specify one or more graph focus nodes, supply a SPARQL query, '
                         'or use the "-A" option',
                         outf.getvalue().strip())
        outf = StringIO()
        with(redirect_stdout(outf)):
            evaluate_cli(f"{rdffile} {shexfile}  -A -s http://example.org/shapes/S".split())
        self.assertEqual("""Errors:
  Focus: http://a.example/s1
  Start: http://example.org/shapes/S
  Reason:   Testing :s1 against shape http://example.org/shapes/S
       No matching triples found for predicate :s4

  Focus: http://a.example/s2
  Start: http://example.org/shapes/S
  Reason:   Testing :s2 against shape http://example.org/shapes/S
       No matching triples found for predicate :s4

  Focus: http://a.example/s3
  Start: http://example.org/shapes/S
  Reason:   Testing :s3 against shape http://example.org/shapes/S
       No matching triples found for predicate :s4""", outf.getvalue().strip())



if __name__ == '__main__':
    unittest.main()
