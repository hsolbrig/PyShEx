import os
import unittest
from pprint import pprint

from pyshex.utils.sparql_query import SPARQLQuery
from tests import datadir


class SparqlQueryTestCase(unittest.TestCase):
    @unittest.skipIf(True, "SPARQL query, sometimes URL is down. Need to look for an alternative.")
    def test_basics(self):
        q = SPARQLQuery('http://wifo5-04.informatik.uni-mannheim.de/drugbank/sparql',
                        os.path.join(datadir, 't1.sparql'))
        self.assertEqual([
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00001',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00002',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00003',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00004',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00005',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00006',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00007',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00008',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00009',
            'http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/DB00010'],
            [str(f) for f in q.focus_nodes()])


if __name__ == '__main__':
    unittest.main()
