import os
import unittest
from contextlib import redirect_stdout
from io import StringIO

from pyshex.shex_evaluator import evaluate_cli

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


# Note: This is a fragile test, as the endpoint below is not stabile.  You may need to add a skip to it in the
# not too distant future
class InlineSPARQLIssue(unittest.TestCase):

    @unittest.skipIf(True, "Fragile endpoint - has BNODES at the moment.  This also takes a looong time")
    def test_inline_rdf(self):
        """ Issue #28. Make sure inline SPARQL with no carriage return works """
        shex = os.path.join(data_dir, 'biolink-model.shex')
        sparql = 'select ?item where{graph ?g {?item a <http://w3id.org/biolink/vocab/Protein>}}'

        # This raises an InvalidSchema error
        messages = StringIO()
        with redirect_stdout(messages):
            evaluate_cli((['-ss', '-sq', sparql, 'http://graphdb.dumontierlab.com/repositories/ncats-red-kg',
                           shex, '-ut', '-pb']))
        print(messages.getvalue())


if __name__ == '__main__':
    unittest.main()
