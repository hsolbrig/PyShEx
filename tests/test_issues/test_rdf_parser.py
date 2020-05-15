import os
import unittest

from rdflib import Graph

from tests import datadir

""" Test for an error in the RDFLIB parser.  To fix the bug in rdflib 4.2.2:
> rdflib.plugins.parsers.notation3.py

1578            k = 'abfrtvn\\"\''.find(ch)
                if k >= 0:
                    uch = '\a\b\f\r\t\v\n\\"\''[k]
"""


class RDFLIBTestCase(unittest.TestCase):
    def test_parser(self):
        rdff = os.path.join(datadir, 'validation', 'Is1_Ip1_LSTRING_LITERAL1_with_all_punctuation.ttl')
        with open(rdff, 'rb') as f:
            rdf = f.read().decode()
        Graph().parse(data=rdf, format="turtle")
        self.assertTrue(True, "Parser has been fixed")


if __name__ == '__main__':
    unittest.main()
