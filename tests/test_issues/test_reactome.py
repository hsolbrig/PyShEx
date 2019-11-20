import unittest

import os

from tests.utils.wikidata_utils import WikiDataTestCase


class ReactomeTestCase(WikiDataTestCase):
    # This will change over time - expected values for the first 8 results
    # Note: This test has never been run past 1
    expected_results = [True, False, False, False, False, True, False, False]

    @unittest.skipIf(False, "Awaiting User-Agent fix (issue 52)")
    def test_wikidata_reactome(self):
        test_data_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'wikidata', 'reactome'))

        rslts = self.run_test(
            "https://raw.githubusercontent.com/shexSpec/schemas/master/Wikidata/pathways/Reactome/manifest_all.json",
            num_entries=1, debug=False, debug_slurps=False, save_graph_dir=test_data_base)
        for rslt in rslts:
            print(f"{'CONFORMS' if rslt.result else 'FAIL'}: {rslt.focus}")
        self.assertTrue(all(expected == actual for expected, actual in zip([r.result for r in rslts],
                                                                            self.expected_results)))


if __name__ == '__main__':
    unittest.main()
