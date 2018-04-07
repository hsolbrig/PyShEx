import unittest

import os

from tests.utils.wikidata_utils import WikiDataTestCase


class ReactomeTestCase(WikiDataTestCase):

    def test_wikidata_reactome(self):
        test_data_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'wikidata', 'reactome'))

        rslts = self.run_test(
            "https://raw.githubusercontent.com/shexSpec/schemas/master/Wikidata/pathways/Reactome/manifest_all.json",
            num_entries=1, debug=False, debug_slurps=False, save_graph_dir=test_data_base)
        for rslt in rslts:
            print(f"{'CONFORMS' if rslt.result else 'FAIL'}: {rslt.focus}")
        self.assertTrue(all(r.result for r in rslts))


if __name__ == '__main__':
    unittest.main()
