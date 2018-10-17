import unittest

from rdflib import Graph

from tests import RDFLIB_PARSING_ISSUE_FIXED

""" Test for an error in the RDFLIB parser.  To fix the bug in rdflib 4.2.2:
> rdflib.plugins.parsers.notation3.py

1578            k = 'abfrtvn\\"\''.find(ch)
                if k >= 0:
                    uch = '\a\b\f\r\t\v\n\\"\''[k]
"""


class RDFLIBTestCase(unittest.TestCase):
    @unittest.skipIf(not RDFLIB_PARSING_ISSUE_FIXED, "Waiting for RDFLIB quote fix")
    def test_parser(self):
        rdff = "/users/hsolbri1/git/shexSpec/shexTest/validation/Is1_Ip1_LSTRING_LITERAL1_with_all_punctuation.ttl"
        with open(rdff, 'rb') as f:
            rdf = f.read().decode()
        Graph().parse(data=rdf, format="turtle")
        self.assertTrue(True, "Parser has been fixed")


if __name__ == '__main__':
    unittest.main()
