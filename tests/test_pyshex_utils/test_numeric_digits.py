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
        self.assertEqual(0, fraction_digits(Literal(117, datatype=XSD.float)))
        # Note: rdflib creates a type of XSD.double, which is NOT derived from decimal (!)
        self.assertEqual(0, fraction_digits(Literal(5.0)))
        self.assertEqual(0, fraction_digits(Literal(5.0, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal(5.55, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal('5.55', datatype=XSD.decimal)))
        self.assertEqual(0, fraction_digits(Literal(-5.0)))
        self.assertEqual(0, fraction_digits(Literal(-5.0, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal(-5.55, datatype=XSD.decimal)))
        self.assertEqual(2, fraction_digits(Literal('-5.55', datatype=XSD.decimal)))
        self.assertIsNone(fraction_digits(XSD.decimal))
        self.assertIsNone(fraction_digits(Literal('abc', datatype=XSD.decimal)))


if __name__ == '__main__':
    unittest.main()
