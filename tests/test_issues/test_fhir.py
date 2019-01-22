import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from pyshex.shex_evaluator import evaluate_cli


class FHIRServerTestCase(unittest.TestCase):

    @unittest.skipIf(True, "Issue 26 needs to be fixed")
    def test_observation(self):
        """ Test online FHIR example """
        outf = StringIO()
        with(redirect_stdout(outf)):
            evaluate_cli("http://hl7.org/fhir/observation-example.ttl http://build.fhir.org/observation.shex -A")
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
