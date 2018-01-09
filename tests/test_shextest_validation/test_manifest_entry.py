import unittest

import os

from ShExJSG import ShExJ
from rdflib import URIRef

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import ShapeAssociation, FixedShapeMap
from tests.utils.manifest import ShExManifest, SHT
from tests.utils.uri_redirector import URIRedirector

ENTRY_NAME = ''
START_AFTER = ''
CONTINUE_ON_FAIL = False
VERBOSE = True
DEBUG = False

BNODE_ISSUE = "Blank Nodes are not preserved in RDF"
RDFLIB_QUOTE = "rdflib not parsing single quote escapes correctly"
AWAIT_FANCY_STUFF = "Too crazy for the first pass"
CRLF_ISSUE = "Code expects crlf and not parsed that way"
DIGITS_ISSUE = "Fraction digits should fail"
NO_JSON = "No json representation of schema is available"
NON_EXISTENT_FOCUS = "Focus node in manifest doesn't exist"

skip_traits = [SHT.LexicalBNode]

expected_failures = {
     "bnode1dot_pass-others_lexicallyEarlier": BNODE_ISSUE,
     "1val1STRING_LITERAL1_with_all_punctuation_pass": RDFLIB_QUOTE,
     "1val1STRING_LITERAL1_with_all_controls_fail": RDFLIB_QUOTE,
     "1val1STRING_LITERAL1_with_all_punctuation_fail": RDFLIB_QUOTE,
     "1val1DOUBLE_pass": "0E0 is not a valid RDF double value",
     "1val1DOUBLElowercase_pass": "0e0 is not a valid RDF double value",
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
     "1nonliteralPattern_pass-bnode-long": BNODE_ISSUE,
     "1NOTIRI_passLv": NO_JSON,
     "1NOTIRI_failIo1": NO_JSON,
     "3groupdotExtra3NLex_pass-iri2": NON_EXISTENT_FOCUS,
     "1focusBNODE_dot_pass": BNODE_ISSUE,
     "1focusPatternB-dot_pass-bnode-long": BNODE_ISSUE,
     "1focusMinLength-dot_pass-bnode-long": BNODE_ISSUE,
     "1focusBNODELength_dot_pass": BNODE_ISSUE

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
        cls.started = not bool(START_AFTER)

    @staticmethod
    def URIname(uri: URIRef) -> str:
        return str(uri).replace(str(SHT), '')

    def eval_entry(self, entry_name: str) -> bool:
        mes = self.mfst.entries[entry_name]
        for me in mes:
            if not self.started and me.name != START_AFTER:
                return True
            else:
                self.started = True
            if me.traits.intersection(skip_traits):
                print(f"Skipping {me.name} ({', '.join([self.URIname(t) for t in me.traits])}) - Skipped trait")
                return True
            elif me.name in expected_failures:
                print(f"Skipping {me.name} ({', '.join([self.URIname(t) for t in me.traits])})"
                      f" - {expected_failures[me.name]}")
                return True
            else:
                if VERBOSE:
                    print(f"Testing {me.name} ({'P' if me.should_pass else 'F'}): {me.schema_uri} - {me.data_uri}")
                d, s = me.data_graph(), me.shex_schema()
                # TODO: straghten this out
                if not d or not s:
                    return True
                cntxt = Context(me.data_graph(), me.shex_schema())
                cntxt.debug_context.trace_nodeSatisfies = cntxt.debug_context.trace_satisfies = \
                    cntxt.debug_context.trace_matches = DEBUG
                map_ = FixedShapeMap()
                map_.add(ShapeAssociation(me.focus, ShExJ.IRIREF(me.shape)))
                test_result = isValid(cntxt, map_) or not me.should_pass
                if not VERBOSE and not test_result:
                    print(f"Testing {me.name} ({'P' if me.should_pass else 'F'}): {me.schema_uri} - {me.data_uri}")
                return test_result

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
