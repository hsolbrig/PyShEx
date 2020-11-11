import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from pyshex.shex_evaluator import evaluate_cli


class FHIRServerTestCase(unittest.TestCase):

    def test_observation_online(self):
        """ Test online FHIR example """
        source_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
        result = os.path.join(source_dir, 'example-haplotype2_online.results')
        outf = StringIO()
        with(redirect_stdout(outf)):
            evaluate_cli("http://hl7.org/fhir/observation-example-haplotype2.ttl "
                         "http://build.fhir.org/observation.shex "
                         "-fn http://hl7.org/fhir/Observation/example-haplotype2")
        if not os.path.exists(result):
            with open(result, 'w') as f:
                f.write(outf.getvalue())
            self.assertTrue(False, "Created test file -- rerun ")
        with open(result) as f:
            self.assertEqual(f.read(), outf.getvalue())

    def test_observation(self):
        """ Test of local FHIR example """
        source_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
        rdf = os.path.join(source_dir, 'example-haplotype2.ttl')
        shex = os.path.join(source_dir, 'observation.shex')
        result = os.path.join(source_dir, 'example-haplotype2.results')
        outf = StringIO()
        with(redirect_stdout(outf)):
            evaluate_cli(f"{rdf} {shex} -fn http://hl7.org/fhir/Observation/example-haplotype2")
        if not os.path.exists(result):
            with open(result, 'w') as f:
                f.write(outf.getvalue())
            self.assertTrue(False, "Created test file -- rerun ")
        with open(result) as f:
            self.assertEqual(f.read(), outf.getvalue())

if __name__ == '__main__':
    unittest.main()
