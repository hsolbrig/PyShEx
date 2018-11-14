import os
import unittest

from rdflib import URIRef

from ancilliary.earlreport import EARLPage
from tests import RDFLIB_PARSING_ISSUE_FIXED
from tests.utils.manifest_tester import ManifestEntryTestCase


class ManifestShexShexCTestCase(ManifestEntryTestCase):
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

    def test_shex_shexc(self):
        self.mfst.shex_format = "shex"
        self.do_test()

    def test_generate_earl_report(self):
        self.mfst.schema_loader.schema_format = "shex"
        earlpage = EARLPage(URIRef("https://github.com/hsolbrig"))
        self.do_test(earlpage)
        earl_report = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', 'earl_report.ttl')
        earlpage.g.serialize(earl_report, format="turtle")
        print(f"EARL report generated in {earl_report}")

if __name__ == '__main__':
    unittest.main()
