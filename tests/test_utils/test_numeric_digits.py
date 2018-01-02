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

from rdflib import Literal, XSD

from pyshex.utils.datatype_utils import total_digits, fraction_digits


class TotalDigitsTestCase(unittest.TestCase):
    def test_total_digits(self):
        self.assertEqual(2, total_digits(Literal(-17)))
        self.assertEqual(2, total_digits(Literal(17)))
        self.assertEqual(1, total_digits(Literal(0)))
        self.assertEqual(1, total_digits(Literal('0.0', datatype=XSD.decimal)))
        self.assertEqual(1, total_digits(Literal(-0.0, datatype=XSD.decimal)))
        self.assertEqual(1, total_digits(Literal(1.0, datatype=XSD.decimal)))
        self.assertEqual(1, total_digits(Literal(-1.0, datatype=XSD.decimal)))
        self.assertEqual(3, total_digits(Literal(5.55, datatype=XSD.decimal)))
        self.assertIsNone(total_digits(Literal('5.55j', datatype=XSD.decimal)))
        self.assertEqual(3, total_digits(Literal('-5.55', datatype=XSD.decimal)))

    @unittest.skipIf(True, "rdflib should never parse 5.55 as an integer, but it does")
    def test_total_digits_2(self):
        self.assertIsNone(total_digits(Literal(5.55, datatype=XSD.integer)))

    def test_fraction_digits(self):
        self.assertEqual(0, fraction_digits(Literal(1)))
        self.assertEqual(0, fraction_digits(Literal(-117253884)))
        self.assertEqual(0, fraction_digits(Literal(127, datatype=XSD.byte)))
        self.assertIsNone(fraction_digits(Literal("Hello")))
        self.assertIsNone(fraction_digits(Literal(117, datatype=XSD.float)))
        # Note: rdflib creates a type of XSD.double, which is NOT derived from decimal (!)
        self.assertIsNone(fraction_digits(Literal(5.0)))
        self.assertEqual(0, fraction_digits(Literal(5.0, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal(5.55, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal('5.55', datatype=XSD.decimal)))
        self.assertIsNone(fraction_digits(Literal(-5.0)))
        self.assertEqual(0, fraction_digits(Literal(-5.0, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal(-5.55, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal('-5.55', datatype=XSD.decimal)))
        self.assertIsNone(fraction_digits(XSD.decimal))
        self.assertIsNone(fraction_digits(Literal('abc', datatype=XSD.decimal)))


if __name__ == '__main__':
    unittest.main()
