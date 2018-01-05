import unittest

import os

from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import ShapeMap, ShapeAssociation, FixedShapeMap
from tests.utils.manifest import ShExManifest


class ManifestEntryTestCase(unittest.TestCase):
    data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'test_utils', 'data')

    def test_manifest_entry(self):
        mfst = ShExManifest(os.path.join(self.data_dir, 'manifest.ttl'), fmt="turtle")
        me = mfst.entries['0_empty'][0]
        cntxt = Context(me.data_graph(), me.shex_schema())
        map = FixedShapeMap()
        map.add(ShapeAssociation(me.focus, ShExJ.IRIREF(me.shape)))
        self.assertTrue(isValid(cntxt, map))


if __name__ == '__main__':
    unittest.main()
