import os
import unittest

from rdflib import Graph

ttl_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'Is1_Ip1_L_with_REGEXP_escapes_bare.ttl'))


class CRLFTestCase(unittest.TestCase):
    def test_crlf(self):
        """ Make sure that the data is being read in raw form -- that linefeeds aren't being stripped """
        g = Graph()
        g.load(ttl_file, format='turtle')
        self.assertEqual('/\t\n\r-\\a𝒸', list(g.objects())[0].value)

if __name__ == '__main__':
    unittest.main()
