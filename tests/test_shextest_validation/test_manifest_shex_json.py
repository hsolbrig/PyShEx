import unittest

from tests.utils.manifest_tester import ManifestEntryTestCase


class ManifestShexJsonTestCase(ManifestEntryTestCase):
    def test_shex_json(self):
        self.mfst.schema_loader.schema_format = "json"
        self.do_test()


if __name__ == '__main__':
    unittest.main()
