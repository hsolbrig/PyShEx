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
