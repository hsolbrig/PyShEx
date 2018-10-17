import unittest

from tests import RDFLIB_PARSING_ISSUE_FIXED
from tests.utils.manifest_tester import ManifestEntryTestCase


class ManifestShexJsonTestCase(ManifestEntryTestCase):
    def __init__(self, methodname):
        if not RDFLIB_PARSING_ISSUE_FIXED:
            issue_text = 'RDFLIB quote parsing issue not fixed'
            skips = {'1val1STRING_LITERAL1_with_all_punctuation_pass': issue_text,
                     '1val1STRING_LITERAL1_with_all_punctuation_fail': issue_text,
                     '1val1STRING_LITERAL1_with_ECHAR_escapes_pass': issue_text,
                     '1val1STRING_LITERAL1_with_ECHAR_escapes_fail': issue_text,
                     '1literalPattern_with_all_punctuation_pass': issue_text,
                     '1literalPattern_with_all_punctuation_fail': issue_text
                     }
        else:
            skips = None
        super().__init__(methodname, skips)

    def test_shex_json(self):
        self.mfst.schema_loader.schema_format = "json"
        self.do_test()


if __name__ == '__main__':
    unittest.main()
