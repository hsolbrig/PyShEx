import unittest

import os

from ShExJSG import ShExJ
from rdflib import URIRef

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import ShapeAssociation, FixedShapeMap
from tests.utils.manifest import ShExManifest
from tests.utils.uri_redirector import URIRedirector

ENTRY_NAME = ''
CONTINUE_ON_FAIL = False

expected_failures = {"bnode1dot_pass-others_lexicallyEarlier": "Blank Nodes are not preserved in RDF",
                     "1bnode_pass-bnode": "Blank Nodes are not preserved in RDF",
                     "1datatype_pass": "Spec says that this shouldn't (or doesn't have to) pass"}


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
            cntxt = Context(me.data_graph(), me.shex_schema())
            map_ = FixedShapeMap()
            map_.add(ShapeAssociation(me.focus, ShExJ.IRIREF(me.shape)))
            print(f"Testing {me.name}: {me.schema_uri} - {me.data_uri}")
            return isValid(cntxt, map_) or not me.should_pass or me.name in expected_failures

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
