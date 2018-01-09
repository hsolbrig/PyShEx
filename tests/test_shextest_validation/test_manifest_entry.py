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
CONTINUE_ON_FAIL = True
VERBOSE = False
DEBUG = False

# Reasons for skipping things
BNODE_ISSUE = "Blank Nodes are not preserved in RDF"
RDFLIB_DOUBLE = "0E0 is not a valid RDF double value"
RDFLIB_QUOTE = "rdflib not parsing single quote escapes correctly"
AWAIT_FANCY_STUFF = "Too crazy for the first pass"
CRLF_ISSUE = "Code expects crlf and not parsed that way"
NO_SHEXTERN = "No JSON representation of shapeExtern.shextern"
USES_IMPORTS = "Uses IMPORTS and no facet saying as much"

skip_traits = [SHT.LexicalBNode, SHT.BNodeShapeLabel, SHT.relativeIRI, SHT.Import, SHT.ShapeMap, SHT.ToldBNode]

expected_failures = {
     "1val1STRING_LITERAL1_with_all_punctuation_pass": RDFLIB_QUOTE,
     "1val1STRING_LITERAL1_with_all_controls_fail": RDFLIB_QUOTE,
     "1val1STRING_LITERAL1_with_all_punctuation_fail": RDFLIB_QUOTE,
     "1val1DOUBLE_pass": RDFLIB_DOUBLE,
     "1val1DOUBLElowercase_pass": RDFLIB_DOUBLE,
     "1literalPattern_with_all_punctuation_pass": RDFLIB_QUOTE,
     "1literalPattern_with_all_punctuation_fail": RDFLIB_QUOTE,
     "1literalPattern_with_REGEXP_escapes_bare_pass": CRLF_ISSUE,
     "1literalPattern_with_ascii_boundaries_pass": AWAIT_FANCY_STUFF,
     "1literalPattern_with_ascii_boundaries_fail": AWAIT_FANCY_STUFF,
     "1literalPattern_with_REGEXP_escapes_pass_bare": CRLF_ISSUE,
     "shapeExtern_fail": NO_SHEXTERN,
     "shapeExtern_pass": NO_SHEXTERN,
     "shapeExternRef_pass": NO_SHEXTERN,
     "shapeExternRef_fail": NO_SHEXTERN,
     "skipped": "Invalid JSON -- 'id' tag in outermost level",
     "repeated-group": "Needs smarter partition processor",
     "1valExprRef-IV1_fail-lit-short": USES_IMPORTS,
     "1valExprRef-IV1_pass-lit-equal": USES_IMPORTS,
     "1valExprRefbnode-IV1_fail-lit-short": USES_IMPORTS,
     "1valExprRefbnode-IV1_pass-lit-equal": USES_IMPORTS,
     "2EachInclude1-IS2_pass": USES_IMPORTS

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
        cls.npassed = 0
        cls.nskipped = 0
        cls.nfailed = 0

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
                if VERBOSE:
                    print(f"Skipping {me.name} ({', '.join([self.URIname(t) for t in me.traits])}) - Skipped trait")
                self.nskipped += 1
                return True
            elif me.name in expected_failures:
                if VERBOSE:
                    print(f"Skipping {me.name} ({', '.join([self.URIname(t) for t in me.traits])})"
                          f" - {expected_failures[me.name]}")
                self.nskipped += 1
                return True
            else:
                if VERBOSE:
                    print(f"Testing {me.name} ({'P' if me.should_pass else 'F'}): {me.schema_uri} - {me.data_uri}")
                d, s = me.data_graph(), me.shex_schema()
                if d is None and me.data_uri:
                    if VERBOSE:
                        print("\t ERROR: Unable to load data file")
                    self.nskipped += 1
                    return True
                if not s:
                    if VERBOSE:
                        print("\t ERROR: Unable to load schema")
                    self.nskipped += 1
                    return True
                cntxt = Context(me.data_graph(), me.shex_schema(), me.extern_shape_for)
                cntxt.debug_context.trace_nodeSatisfies = cntxt.debug_context.trace_satisfies = \
                    cntxt.debug_context.trace_matches = DEBUG
                map_ = FixedShapeMap()
                map_.add(ShapeAssociation(me.focus, ShExJ.IRIREF(me.shape)))
                test_result = isValid(cntxt, map_) or not me.should_pass
                if not VERBOSE and not test_result:
                    print(f"Failed {me.name} ({'P' if me.should_pass else 'F'}): {me.schema_uri} - {me.data_uri}")
                if test_result:
                    self.npassed += 1
                else:
                    if VERBOSE:
                        print("\t**** FAIL *****")
                    self.nfailed += 1
                return test_result

    def test_manifest(self):
        if ENTRY_NAME:
            rslt = self.eval_entry(ENTRY_NAME)
        else:
            if CONTINUE_ON_FAIL:
                rslt = all([self.eval_entry(k) for k in self.mfst.entries.keys()])
            else:
                rslt = all(self.eval_entry(k) for k in self.mfst.entries.keys())

        print(f"\n{self.nfailed + self.npassed + self.nskipped} Tests\n\t{self.npassed} "
              f"Passed\n\t{self.nfailed} Failed\n\t{self.nskipped} Skips")
        self.assertTrue(rslt)


if __name__ == '__main__':
    unittest.main()
