import unittest

import os
from rdflib import RDF

from pyshex.utils.schema_loader import SchemaLoader

schemas_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'schemas'))

class SchemaLoaderTestCase(unittest.TestCase):
    def test_loads_shexc(self):
        """ Load a schema string and test a couple of elements """
        loader = SchemaLoader()
        schema = loader.loads("""<http://a.example/S1> {
   ( <http://a.example/p1> .|
     <http://a.example/p2> .|
     <http://a.example/p3> .|
     <http://a.example/p4> .
   ){2,3}
}""")
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)
        self.assertEqual({"http://a.example/p1",
                          "http://a.example/p2",
                          "http://a.example/p3",
                          "http://a.example/p4"}, {e.predicate for e in schema.shapes[0].expression.expressions})

    def test_loads_shexj(self):
        """ Load a schema string and test a couple of elements """
        loader = SchemaLoader()
        schema = loader.loads("""{
  "@context": "http://www.w3.org/ns/shex.jsonld",
  "type": "Schema",
  "shapes": [
    {
      "id": "http://a.example/S1",
      "type": "Shape",
      "expression": {
        "type": "TripleConstraint",
        "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
      }
    }
  ]
}""")
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)
        self.assertEqual(str(RDF.type), schema.shapes[0].expression.predicate)

    def test_load_shexc(self):
        loader = SchemaLoader()

        # Local file name
        fileloc = os.path.join(schemas_dir, 'startCode3.shex')
        schema = loader.load(fileloc)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # Local file object
        with open(fileloc) as f:
            _ = loader.load(f)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # URL
        fileurl = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemas/startCode3.shex"
        schema = loader.load(fileurl)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

    def test_load_shexj(self):
        loader = SchemaLoader()

        # Local file name
        fileloc = os.path.join(schemas_dir, 'startCode3.json')
        schema = loader.load(fileloc)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # Local file object
        with open(fileloc) as f:
            _ = loader.load(f)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # URL
        fileurl = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemas/startCode3.json"
        schema = loader.load(fileurl)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

    def test_location_rewrite(self):
        loader = SchemaLoader()
        # Note: Deliberately a bad URL to make sure this works
        loader.root_location = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemasz/"
        loader.redirect_location = schemas_dir + '/'
        fileloc = loader.root_location + 'startCode3.shex'
        schema = loader.load(fileloc)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

    def test_format_change(self):
        loc = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemas/startCode3"
        loader = SchemaLoader(schema_type_suffix='json')
        self.assertEqual(f"{loc}.json", loader.location_rewrite(f"{loc}.shex"))
        self.assertEqual(f"{loc}.jsontern", loader.location_rewrite(f"{loc}.shextern"))
        loader.schema_format = 'shex'
        self.assertEqual(f"{loc}.shex", loader.location_rewrite(f"{loc}.shex"))
        self.assertEqual(f"{loc}.shextern", loader.location_rewrite(f"{loc}.shextern"))
        self.assertEqual(f"{loc}.shextern", loader.location_rewrite(f"{loc}.jsontern"))


if __name__ == '__main__':
    unittest.main()
