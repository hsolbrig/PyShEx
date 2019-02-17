import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from pyshex import PrefixLibrary
from pyshex.shex_evaluator import evaluate_cli


class BPM2TestCase(unittest.TestCase):

    def test_fail(self):
        """ Test max cardinality of 0 AND error reporting """
        datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        shexpath = os.path.join(datadir, 'issue_20.shex')
        rdfpath = os.path.join(datadir, 'issue_20.ttl')
        expectedpath = os.path.join(datadir, 'issue_20.errors')

        pl = PrefixLibrary(rdfpath)
        output = StringIO()
        with redirect_stdout(output):
            evaluate_cli(f"{rdfpath} {shexpath} -fn {pl.EX.BPM1}")
            evaluate_cli(f"{rdfpath} {shexpath} -fn {pl.EX.BPM2}")

        if not os.path.exists(expectedpath):
            with open(expectedpath, 'w') as f:
                f.write(output.getvalue())
            self.assertTrue(False, "Output created, rerun")
        with open(expectedpath) as f:
            expected = f.read()

        self.maxDiff = None
        self.assertEqual(expected, output.getvalue())

if __name__ == '__main__':
    unittest.main()
