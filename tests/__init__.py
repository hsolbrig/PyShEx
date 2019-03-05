
# True means refresh all test files (only partially implemented at the moment)
import os

refresh_files = False

# True means skip the disease test
skip_diseases = True

datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

# Settings for rdflib parsing issue

#         See line 1578 in notation3.py:
#                 k = 'abfrtvn\\"\''.find(ch)
#                 if k >= 0:
#                     uch = '\a\b\f\r\t\v\n\\"\''[k]
from rdflib import __version__ as rdflib_version
RDFLIB_PARSING_ISSUE_FIXED = rdflib_version >= "5.0.0"