import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from pyshex.shex_evaluator import evaluate_cli

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


class ErrorReportingIssue(unittest.TestCase):
    """ Test Issue #30.  Note that this unit test is reasonably fragile, as it counts on an External SPARQL
    endpoint.
    """

    @unittest.skipIf(False, "Fragile test - we need local data to consistently reproduce")
    def test_messages(self):
        """ Test failures with no reasons supplied """
        shex = os.path.join(data_dir, 'biolink-model.shex')
        sparql = os.path.join(data_dir, 'biolink_model.sparql')
        messages = StringIO()
        with redirect_stdout(messages):
            evaluate_cli(f'-ss -sq {sparql}  http://graphdb.dumontierlab.com/repositories/ncats-red-kg {shex} -ut -pb')
        for line in messages.getvalue().split('\n'):
            self.assertFalse(line.strip().endswith('Reason:'))


if __name__ == '__main__':
    unittest.main()
