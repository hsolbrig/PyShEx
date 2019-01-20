import unittest

import os

from tests.utils.wikidata_utils import WikiDataTestCase
from tests import skip_diseases


class WikiDiseasesTestCase(WikiDataTestCase):
    """ Test a sample conformance checker for the WikiData disease structure

    """
    # This will change over time - expected values for the first 8 results
    expected_results = [True, True, True, True, True, True, True, True]

    @unittest.skipIf(skip_diseases, "Wikidata disease test disabled")
    def test_diseases(self):
        test_data_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'wikidata', 'disease'))

        rslts = self.run_test("https://raw.githubusercontent.com/SuLab/Genewiki-ShEx/master/diseases/manifest_100.json",
                              num_entries=8, debug=False, debug_slurps=False, save_graph_dir=test_data_base)
        for rslt in rslts:
            print(f"{'CONFORMS' if rslt.result else 'FAIL'}: {rslt.focus}")
        # The following will validate from 1 to 8 entries
        self.assertTrue(all(expected == actual for expected, actual in zip([r.result for r in rslts],
                                                                           self.expected_results)))


if __name__ == '__main__':
    unittest.main()
