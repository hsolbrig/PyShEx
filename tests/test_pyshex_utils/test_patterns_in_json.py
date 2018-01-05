import json
import re
import unittest


class JsonPatternTestCase(unittest.TestCase):
    """
    This test case is used to address issues in the string facets example 2
    """
    def test_non_unicode(self):
        b1 = '^\\t\\\\X\?$'
        b2 = r'^\t\\X\?$'

        self.assertEqual(b1, b2)
        self.assertIsNotNone(re.search(b1, '\t\\X?'))
        self.assertIsNone(re.search(b1, 'a\t\\X?'))
        self.assertIsNone(re.search(b1, '\t\\X?z'))

        escaped_b1 = re.sub(r'\\', r'\\\\', b1)
        bj1 = f'{{"pattern" : "{escaped_b1}"}}'
        json_b1 = json.loads(bj1)
        self.assertIsNotNone(re.search(json_b1['pattern'], '\t\\X?'))

    def test_unicode(self):
        b1 = '^\\t\\\\𝒸\?$'
        b2 = r'^\t\\𝒸\?$'

        self.assertEqual(b1, b2)
        self.assertIsNotNone(re.search(b1, '\t\\𝒸?'))
        self.assertIsNone(re.search(b1, 'a\t\\𝒸?'))
        self.assertIsNone(re.search(b1, '\t\\𝒸?z'))

        escaped_b1 = re.sub(r'\\', r'\\\\', b1)
        bj1 = f'{{"pattern" : "{escaped_b1}"}}'
        json_b1 = json.loads(bj1)
        self.assertIsNotNone(re.search(json_b1['pattern'], '\t\\𝒸?'))

    def test_unicode_2(self):
        b1 = '^\\t\\\\\U0001D4B8\?$'
        b2 = r'^\t\\𝒸\?$'

        self.assertEqual(b1, b2)
        self.assertIsNotNone(re.search(b1, '\t\\\U0001D4B8?'))
        self.assertIsNone(re.search(b1, 'a\t\\\U0001D4B8?'))
        self.assertIsNone(re.search(b1, '\t\\\U0001D4B8?z'))

        escaped_b1 = re.sub(r'\\', r'\\\\', b1)
        bj1 = f'{{"pattern" : "{escaped_b1}"}}'
        json_b1 = json.loads(bj1)
        self.assertIsNotNone(re.search(json_b1['pattern'], '\t\\\U0001D4B8?'))


if __name__ == '__main__':
    unittest.main()
