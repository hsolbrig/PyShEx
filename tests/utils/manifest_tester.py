import unittest

import os
from typing import Dict

import sys
from ShExJSG import ShExJ
from rdflib import URIRef

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import ShapeAssociation, FixedShapeMap, START
from tests.utils.manifest import ShExManifest, SHT, validation_dir
from tests.utils.uri_redirector import URIRedirector

# TODO: Remove this whenever rdflib issue #124 is fixed (https://github.com/RDFLib/rdflib/issues/804)
sys.setrecursionlimit(1200)

ENTRY_NAME = ''              # Individual element to test
START_AFTER = ''             # Element to start at (or after)

CONTINUE_ON_FAIL = True
VERBOSE = False
DEBUG = bool(ENTRY_NAME)
TEST_SKIPS_ONLY = False                  # Double check that all skips need skipping

# Local equivalent of online data files
LOCAL_FILE_LOC = os.path.expanduser("~/git/shexTest/")
# LOCAL_FILE_LOC = ''

# Do Not Change this - must match manifest
REMOTE_FILE_LOC = "https://raw.githubusercontent.com/shexSpec/shexTest/master/"

# Reasons for skipping things
USES_IMPORTS = "Uses IMPORTS and no facet saying as much"
LONG_UCHAR = "Uses multi-byte literals"
RDFLIB_ISSUE = "RDFLIB single quote parsing error"
FALSE_LEAD_ISSUE = "Unknown issue with false lead"
FOCUS_DATATYPE = "FocusDatatype"
GREEDY_ISSUE = "Greedy issue - needs resolution"

skip_traits = [SHT.Import, SHT.Include, SHT.BNodeShapeLabel, SHT.ShapeMap, SHT.OutsideBMP,
               SHT.ToldBNode, SHT.LexicalBNode]

# We can't do an effective test on relative files when we're rewriting URI's
if LOCAL_FILE_LOC:
    skip_traits.append(SHT.relativeIRI)

# NOTE: A lot of expected failures aren't included in this list, as, at the moment, we just fail and don't say why.
# skipped test fails json only
expected_failures = {
     "skipped": USES_IMPORTS,
     "1valExprRef-IV1_pass-lit-equal": USES_IMPORTS,
     "1valExprRefbnode-IV1_fail-lit-short": USES_IMPORTS,
     "1valExprRefbnode-IV1_pass-lit-equal": USES_IMPORTS,
     "1val1STRING_LITERAL1_with_ECHAR_escapes_fail": LONG_UCHAR,
     "1val1STRING_LITERAL1_with_ECHAR_escapes_pass": LONG_UCHAR,
     "1val1STRING_LITERAL1_with_all_punctuation_fail": RDFLIB_ISSUE,
     "1val1STRING_LITERAL1_with_all_punctuation_pass": RDFLIB_ISSUE,
     "focusdatatype_pass": FOCUS_DATATYPE,
     "focusdatatype_pass-empty": FOCUS_DATATYPE,
     "1focusvsORdatatype_pass-dt": FOCUS_DATATYPE,
}


class ManifestEntryTestCase(unittest.TestCase):
    """
    Base class for manifest tests
    """

    @classmethod
    def setUpClass(cls):
        cls.mfst = ShExManifest(os.path.join(validation_dir, 'manifest.ttl'), manifest_format="turtle")
        if LOCAL_FILE_LOC:
            cls.mfst.schema_loader.base_location = REMOTE_FILE_LOC
            cls.mfst.schema_loader.redirect_location = LOCAL_FILE_LOC
            cls.mfst.data_redirector = URIRedirector(URIRef(REMOTE_FILE_LOC), LOCAL_FILE_LOC)
        cls.started = not bool(START_AFTER)
        cls.npassed = 0
        cls.nskipped = 0
        cls.nfailed = 0
        cls.start_skipped = 0
        cls.skip_reasons: Dict[str, int] = {}

    @staticmethod
    def URIname(uri: URIRef) -> str:
        return str(uri).replace(str(SHT), '')

    def eval_entry(self, entry_name: str) -> bool:
        mes = self.mfst.entries[entry_name]
        for me in mes:                          # There can be more than one entry per name...
            # Determine the start point
            if not self.started:
                if me.name != START_AFTER:
                    self.start_skipped += 1
                    return True
                else:
                    self.started = True
                    if VERBOSE:
                        print(f"STARTED - Skipped {self.start_skipped} entries")

            # Determine whether this entry should be skipped
            should_skip = False

            # Skip
            skipped_traits = list(me.traits.intersection(skip_traits))
            if skipped_traits:
                if VERBOSE:
                    print(f"Skipping {me.name} ({', '.join([self.URIname(t) for t in me.traits])}) - Skipped trait")
                key = str(skipped_traits[0]).replace(str(SHT), 'sht:')
                if key not in self.skip_reasons:
                    self.skip_reasons[key] = 0
                self.skip_reasons[key] = self.skip_reasons[key] + 1
                self.nskipped += 1
                should_skip = True
            elif me.name in expected_failures:
                if VERBOSE:
                    print(f"Skipping {me.name} ({', '.join([self.URIname(t) for t in me.traits])})"
                          f" - {expected_failures[me.name]}")
                key = expected_failures[me.name]
                if key not in self.skip_reasons:
                    self.skip_reasons[key] = 0
                self.skip_reasons[key] = self.skip_reasons[key] + 1
                self.nskipped += 1
                should_skip = True
            if should_skip and not TEST_SKIPS_ONLY:
                return True
            if TEST_SKIPS_ONLY and not should_skip:
                return True

            # Validate the entry
            if VERBOSE:
                shex_uri = self.mfst.schema_loader.location_rewrite(me.schema_uri)
                data_uri = self.mfst.data_redirector.uri_for(me.data_uri) \
                    if self.mfst.data_redirector else me.data_uri
                print(f"Testing {me.name} ({'P' if me.should_pass else 'F'}): {shex_uri} - {data_uri}")
            g, s = me.data_graph(), me.shex_schema()
            if g is None and me.data_uri:
                print("\t ERROR: Unable to load data file")
                print(f"\t TRAITS: ({','.join(me.traits)})")
                self.nskipped += 1
                return True
            if not s:
                print("\t ERROR: Unable to load schema")
                print(f"\t TRAITS: ({','.join(me.traits)})")
                self.nskipped += 1
                return True
            cntxt = Context(g, s, me.extern_shape_for)
            cntxt.debug_context.debug = DEBUG
            map_ = FixedShapeMap()
            focus = self.mfst.data_redirector.uri_for(me.focus)
            if ':' not in focus:
                focus = "file://" + focus
            map_.add(ShapeAssociation(URIRef(focus), ShExJ.IRIREF(me.shape) if me.shape else START))
            rslt = isValid(cntxt, map_)
            test_result, reasons = rslt[0] or not me.should_pass, rslt[1]

            # Analyze the result
            if not VERBOSE and not test_result:
                print(f"Failed {me.name} ({'P' if me.should_pass else 'F'}): {me.schema_uri} - {me.data_uri}")
                print(f"\t TRAITS: ({','.join(me.traits)})")
            if test_result:
                self.npassed += 1
            else:
                if VERBOSE:
                    print("\t**** FAIL *****")
                    print(f"\t TRAITS: ({','.join(me.traits)})")
                self.nfailed += 1
            return test_result

    def do_test(self):
        if ENTRY_NAME:
            rslt = self.eval_entry(ENTRY_NAME)
        else:
            if CONTINUE_ON_FAIL:
                rslt = all([self.eval_entry(k) for k in self.mfst.entries.keys()])
            else:
                rslt = all(self.eval_entry(k) for k in self.mfst.entries.keys())

        print(f"\n{self.nfailed + self.npassed + self.nskipped} Tests\n\t{self.npassed} "
              f"Passed\n\t{self.nfailed} Failed\n\t{self.nskipped} Skips")

        from pprint import PrettyPrinter
        pp = PrettyPrinter().pprint
        pp(self.skip_reasons)
        self.assertTrue(rslt)
