# Copyright (c) 2018, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest

import os
from rdflib import RDF

from pyshex.utils.schema_loader import SchemaLoader


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
        fileloc = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data', 'startCode3.shex')
        schema = loader.load(fileloc)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # Local file object
        with open(fileloc) as f:
            schema2 = loader.load(f)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # URL
        fileurl = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemas/startCode3.shex"
        schema = loader.load(fileurl)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

    def test_load_shexj(self):
        loader = SchemaLoader()

        # Local file name
        fileloc = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data', 'startCode3.json')
        schema = loader.load(fileloc)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # Local file object
        with open(fileloc) as f:
            schema2 = loader.load(f)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

        # URL
        fileurl = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemas/startCode3.json"
        schema = loader.load(fileurl)
        self.assertEqual("http://a.example/S1", schema.shapes[0].id)

    def test_location_rewrite(self):
        loader = SchemaLoader()
        # Note: Deliberately a bad URL to make sure this works
        loader.base_location = "https://raw.githubusercontent.com/shexSpec/shexTest/2.0/schemasz/"
        loader.redirect_location = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data') + '/'
        fileloc = loader.base_location + 'startCode3.shex'
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
