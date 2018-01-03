# Copyright (c) 2017, Mayo Clinic
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

from ShExJSG import ShExJ
from rdflib import Literal

from pyshex.utils.schema_utils import reference_of
from tests.utils.setup_test import setup_test, setup_context

shex_1 = """{ "type": "Schema", "shapes": [
    { "id": "http://schema.example/IntConstraint",
      "type": "NodeConstraint",
      "datatype": "http://www.w3.org/2001/XMLSchema#integer"
    } ] }"""


class SimpleExamplesTestCase(unittest.TestCase):
    def test_example_1(self):
        from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
        cntxt = setup_context(shex_1, None)
        self.assertTrue(satisfies(, Literal('"30"^^<http://www.w3.org/2001/XMLSchema#integer>'), reference_of(schema,
                                                                                                              ShExJ.IRIREF(
                                                                                                                  "http://schema.example/IntConstraint")))
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
