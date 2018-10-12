import unittest
import os

import sys
from ShExJSG import ShExJ
from pyjsg.jsglib import load
from rdflib import URIRef, Namespace, Graph

from tests.utils.manifest import ShExManifest
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
validation_dir = os.path.join(data_dir, 'validation')
schemas_dir = os.path.join(data_dir, 'schemas')
manifest_ttl = os.path.join(validation_dir, 'manifest.ttl')
manifest_json = os.path.join(validation_dir, 'manifest.jsonld')


SHEX = Namespace("http://www.w3.org/ns/shex#")
MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
SHT = Namespace("http://www.w3.org/ns/shacl/test-suite#")
SX = Namespace("https://shexspec.github.io/shexTest/ns#")

entries_list = {
            '0_empty',
            '0_other',
            '0_otherbnode',
            '1Adot_pass',
            '1dot-base_fail-empty',
            '1dot-base_fail-missing',
            '1dot-base_pass-noOthers',
            '1dotLNdefault_pass-noOthers',
            '1dotLNex-HYPHEN_MINUS_pass-noOthers',
            '1dotNS2_pass-noOthers',
            '1dotNSdefault_pass-noOthers',
            '1dotSemi_pass-noOthers',
            '1dot_fail-empty',
            '1dot_fail-missing',
            '1dot_pass-noOthers',
            '1dot_pass-others_lexicallyEarlier',
            '1dot_pass-others_lexicallyLater',
            '1inversedot_fail-empty',
            '1inversedot_fail-missing',
            '1inversedot_pass-noOthers',
            '1inversedot_pass-over_lexicallyEarlier',
            '1inversedot_pass-over_lexicallyLater',
            'bnode1dot_fail-missing',
            'bnode1dot_pass-others_lexicallyEarlier',
            'PstarT'}


# TODO: Remove this once the rdflib list recursion issue is resolved
sys.setrecursionlimit(1200)


class ManifestTestCase(unittest.TestCase):

    def test_basics_ttl(self):
        mfst = ShExManifest(manifest_ttl, 'turtle')
        self.assertEqual(entries_list, set(mfst.entries.keys()).intersection(entries_list))

    def test_basics_jsonld(self):
        mfst = ShExManifest(manifest_json)
        self.assertEqual(entries_list, set(mfst.entries.keys()).intersection(entries_list))

    def attributes_tester(self, mfst: ShExManifest) -> None:
        me = mfst.entries['1dotSemi_pass-noOthers']
        self.assertEqual(1, len(me))
        me = me[0]
        self.assertEqual('1dotSemi_pass-noOthers', me.name)
        self.assertEqual({SHT.TriplePattern}, me.traits)
        self.assertEqual('PREFIX : <http://a.example/> <S1> { :p1 ., } on { <s1> <p1> <o1> }', me.comments)
        self.assertEqual(MF.proposed, me.status)
        self.assertEqual(SHT.ValidationTest, me.entry_type)
        self.assertTrue(me.should_parse)
        self.assertTrue(me.should_pass)
        self.assertEqual(URIRef('https://raw.githubusercontent.com/shexSpec/shexTest/master/schemas/1dotSemi.shex'),
                         me.schema_uri)
        self.assertEqual(URIRef("http://a.example/S1"), me.shape)
        self.assertEqual(
            URIRef('https://raw.githubusercontent.com/shexSpec/shexTest/master/validation/Is1_Ip1_Io1.ttl'),
            me.data_uri)
        self.assertEqual(me.focus, URIRef("http://a.example/s1"))

        me = mfst.entries['bnode1dot_pass-others_lexicallyEarlier'][0]
        self.assertEqual({SHT.BNodeShapeLabel, SHT.TriplePattern}, me.traits)

        me = mfst.entries['1inversedot_fail-empty'][0]
        self.assertEqual({SHT.TriplePattern}, me.traits)
        self.assertTrue(me.should_parse)
        self.assertFalse(me.should_pass)
        self.assertEqual(me.status, MF.proposed)
        self.assertEqual(me.comments, "<S> { ^<p1> . } on {  }")

    def test_attributes_ttl(self):
        mfst = ShExManifest(manifest_ttl, manifest_format="turtle")
        self.attributes_tester(mfst)

    @unittest.skipIf(True, "Issue report #27 filed in shexTest")
    def test_attributes_jsonld(self):
        mfst = ShExManifest(manifest_json)
        self.attributes_tester(mfst)

    def test_shex(self):
        mfst = ShExManifest(manifest_ttl, "turtle")
        me = mfst.entries['1Adot_pass'][0]
        self.assertEqual(URIRef('https://raw.githubusercontent.com/shexSpec/shexTest/master/schemas/1Adot.shex'),
                         me.schema_uri)
        with open(os.path.join(schemas_dir, '1Adot.json')) as shex_file:
            target_shex_file = load(shex_file, ShExJ)
            del target_shex_file['@context']
            self.assertEqual(target_shex_file._as_json, mfst.entries['1Adot_pass'][0].shex_schema()._as_json)

    def test_data(self):
        mfst = ShExManifest(manifest_ttl, 'turtle')
        me = mfst.entries['PstarT'][0]
        g = Graph()
        g.parse(os.path.join(validation_dir, 'Pstar.ttl'), format="turtle")
        self.assertEqual(set(g), set(me.data_graph(fmt="turtle")))

    def test_full_ttl(self):
        mfst = ShExManifest(manifest_ttl, 'turtle')
        self.assertEqual(entries_list, entries_list.intersection(mfst.entries))

    def test_full_json(self):
        mfst = ShExManifest(manifest_json)
        self.assertEqual(entries_list, entries_list.intersection(mfst.entries))

    def test_externs(self):
        mfst = ShExManifest(manifest_ttl, 'turtle')
        me = mfst.entries['shapeExtern_pass'][0]
        self.assertEqual(
            [URIRef('https://raw.githubusercontent.com/shexSpec/shexTest/master/schemas/shapeExtern.shextern')],
            me.externs)
        me = mfst.entries['1Adot_pass'][0]
        self.assertEqual([], me.externs)

    def test_extern_str(self):
        mfst = ShExManifest(manifest_ttl, 'turtle')
        me = mfst.entries['shapeExtern_pass'][0]
        self.assertIsNotNone(me.extern_shape_for(ShExJ.IRIREF("http://a.example/Sext")))


if __name__ == '__main__':
    unittest.main()
