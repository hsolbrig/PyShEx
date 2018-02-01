
import unittest

from tests.utils.manifest_tester import ManifestEntryTestCase


class ManifestShexShexCTestCase(ManifestEntryTestCase):
    def test_shex_shexc(self):
        self.mfst.shex_format = "shex"
        self.do_test()


if __name__ == '__main__':
    unittest.main()
