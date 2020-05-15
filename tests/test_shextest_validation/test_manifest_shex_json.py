import unittest

from tests.utils.manifest_tester import ManifestEntryTestCase


class ManifestShexJsonTestCase(ManifestEntryTestCase):
    def __init__(self, methodname):
        # This is a spot that you can insert conditional skips -- the second parameter below is a dictionary of test
        # names and skip reasons.
        # Example: skips = {'1val1STRING_LITERAL1_with_all_punctuation_pass': issue_text}
        super().__init__(methodname, None)

    def test_shex_json(self):
        self.mfst.schema_loader.schema_format = "json"
        self.do_test()


if __name__ == '__main__':
    unittest.main()
