import unittest

import os

from ShExJSG import ShExJ
from rdflib import URIRef

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import ShapeAssociation, FixedShapeMap
from tests.utils.manifest import ShExManifest
from tests.utils.uri_redirector import URIRedirector

ENTRY_NAME = '1literalFractiondigits_pass-decimal-short'
CONTINUE_ON_FAIL = False

BNODE_ISSUE = "Blank Nodes are not preserved in RDF"
RDFLIB_QUOTE = "rdflib not parsing single quote escapes correctly"
AWAIT_FANCY_STUFF = "Too crazy for the first pass"
CRLF_ISSUE = "Code expects crlf and not parsed that way"

expected_failures = {
     "bnode1dot_pass-others_lexicallyEarlier": BNODE_ISSUE,
     "1bnode_pass-bnode": BNODE_ISSUE,
     "1datatype_pass": "Spec says that this shouldn't (or doesn't have to) pass",
     "1val1STRING_LITERAL1_with_all_punctuation_pass": RDFLIB_QUOTE,
     "1val1STRING_LITERAL1_with_all_controls_fail": RDFLIB_QUOTE,
     "1val1STRING_LITERAL1_with_all_punctuation_fail": RDFLIB_QUOTE,
     "1val1DOUBLE_pass": "0E0 is not a valid RDF double value",
     "1val1DOUBLElowercase_pass": "0e0 is not a valid RDF double value",

     "1literalFractiondigits_pass-integer-short": "5 digits is not 5 fraction digits",
     "1literalFractiondigits_pass-xsd_integer-short": "5 digits is not 5 fraction digits",
     "1literalTotaldigits_pass-decimal-short": "1.234 doesn't have 5 digits(?)",
     "1literalTotaldigits_pass-xsd_integer-short": "ShEx asks for 5 digits, spec gives 4",
     "1literalTotaldigits_pass-byte-short": "ShEx asks for 5 digits, spec gives 4",
     "1bnodeLength_pass-bnode-equal": BNODE_ISSUE,
     "1nonliteralLength_pass-bnode-equal": BNODE_ISSUE,
     "1bnodeMaxlength_pass-bnode-short": BNODE_ISSUE,
     "1bnodeMaxlength_pass-bnode-equal": BNODE_ISSUE,
     "1nonliteralMaxlength_pass-bnode-short": BNODE_ISSUE,
     "1nonliteralMaxlength_pass-bnode-equal": BNODE_ISSUE,
     "1literalPattern_with_all_punctuation_pass": RDFLIB_QUOTE,
     "1literalPattern_with_all_punctuation_fail": RDFLIB_QUOTE,
     "1literalPattern_with_REGEXP_escapes_bare_pass": CRLF_ISSUE,
     "1literalPattern_with_ascii_boundaries_pass": AWAIT_FANCY_STUFF,
     "1literalPattern_with_ascii_boundaries_fail": AWAIT_FANCY_STUFF,
     "1literalPattern_with_REGEXP_escapes_pass_bare": CRLF_ISSUE,
     "1bnodePattern_pass-bnode-match": BNODE_ISSUE,
     "1bnodePattern_fail-bnode-long": BNODE_ISSUE,
     "1nonliteralPattern_pass-bnode-match": BNODE_ISSUE,
     "1nonliteralPattern_pass-bnode-long": BNODE_ISSUE
}


class ManifestEntryTestCase(unittest.TestCase):
    data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'test_utils', 'data')

    @classmethod
    def setUpClass(cls):
        cls.mfst = ShExManifest(os.path.join(cls.data_dir, 'manifest.ttl'), fmt="turtle")
        cls.mfst.schema_redirector = \
            URIRedirector(URIRef("https://raw.githubusercontent.com/shexSpec/shexTest/master/"),
                          "/Users/mrf7578/Development/git/hsolbrig/shexTest/")
        cls.mfst.data_redirector = URIRedirector(URIRef("https://raw.githubusercontent.com/shexSpec/shexTest/master/"),
                                                 "/Users/mrf7578/Development/git/hsolbrig/shexTest/")

    def eval_entry(self, entry_name: str) -> bool:
        mes = self.mfst.entries[entry_name]
        for me in mes:
            if me.name not in expected_failures:
                print(f"Testing {me.name} ({'P' if me.should_pass else 'F'}): {me.schema_uri} - {me.data_uri}")
                cntxt = Context(me.data_graph(), me.shex_schema())
                map_ = FixedShapeMap()
                map_.add(ShapeAssociation(me.focus, ShExJ.IRIREF(me.shape)))
                return isValid(cntxt, map_) or not me.should_pass or me.name in expected_failures
            else:
                print(f"Skipping {me.name} - {expected_failures[me.name]}")
                return True

    def test_manifest(self):
        if ENTRY_NAME:
            self.assertTrue(self.eval_entry(ENTRY_NAME))
        else:
            if CONTINUE_ON_FAIL:
                self.assertTrue(any(self.eval_entry(k) for k in self.mfst.entries.keys()))
            else:
                self.assertTrue(all(self.eval_entry(k) for k in self.mfst.entries.keys()))


if __name__ == '__main__':
    unittest.main()
