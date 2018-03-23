import unittest

import os

from tests.utils.wikidata_utils import WikiDataTestCase


class WikiDiseasesTestCase(WikiDataTestCase):
    """ Test a sample convormance checker for the WikiData disease structure

    """

    def test_diseases(self):
        test_data_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'wikidata', 'disease'))

        # TODO: Entry #9 causes both this process AND shex.js to hang
        rslts = self.run_test("https://raw.githubusercontent.com/SuLab/Genewiki-ShEx/master/diseases/manifest_100.json",
                              num_entries=8, debug=False, debug_slurps=False, save_graph_dir=test_data_base)
        for rslt in rslts:
            print(f"{'CONFORMS' if rslt.result else 'FAIL'}: {rslt.focus}")
        self.assertTrue(all(r.result for r in rslts))


if __name__ == '__main__':
    unittest.main()
