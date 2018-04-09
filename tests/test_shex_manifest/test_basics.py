import unittest

from jsonasobj import loads

from pyshex.shex_manifest.manifest import Manifest

manifest_sample = """{
   "schemaLabel": "bibframe book",
   "schemaURL": "book.shex",
   "dataLabel": "simple",
   "dataURL": "book.ttl",
   "queryMap": "<samples9298996>@<Work>",
   "status": "conformant"
}"""


class ManifestTestCase(unittest.TestCase):
    def test_loader(self):
        manifest = Manifest("https://www.w3.org/2017/10/bibframe-shex/shex-simple-examples.json")
        me = manifest.entries[0]
        self.assertEqual('bibframe book', me.schemaLabel)
        self.assertEqual('book.shex', me.schemaURL)
        self.assertEqual('simple', me.dataLabel)
        self.assertEqual('book.ttl', me.dataURL)
        self.assertEqual('<samples9298996>@<Work>', me.queryMap)
        self.assertEqual('conformant', me.status)
        self.assertEqual(9, len(manifest.entries))


if __name__ == '__main__':
    unittest.main()
