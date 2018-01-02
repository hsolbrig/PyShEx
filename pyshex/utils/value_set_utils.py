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
from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF
from rdflib import URIRef, Literal

from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector


def objectValueMatches(n: nodeSelector, vsv: ShExJ.objectValue) -> bool:
    """ http://shex.io/shex-semantics/#values

    Implements "n = vsv" where vsv is an objectValue and n is a Node

    Note that IRIREF is a string pattern, so the matching type is str
    """
    return \
        (isinstance(vsv, IRIREF) and isinstance(n, URIRef) and uriref_matches_iriref(n, vsv)) or \
        (isinstance(vsv, ShExJ.ObjectLiteral) and isinstance(n, Literal) and literal_matches_objectliteral(n, vsv))


def uriref_matches_iriref(v1: URIRef, v2: ShExJ.IRIREF) -> bool:
    """ Compare :py:class:`rdflib.URIRef` value with :py:class:`ShExJ.IRIREF` value """
    return str(v1) == str(v2)


def uriref_startswith_iriref(v1: URIRef, v2: ShExJ.IRIREF) -> bool:
    """ Determine whether a :py:class:`rdflib.URIRef` value starts with the text of a :py:class:`ShExJ.IRIREF` value """
    return str(v1).startswith(str(v2))


def literal_matches_objectliteral(v1: Literal, v2: ShExJ.ObjectLiteral) -> bool:
    """ Compare :py:class:`rdflib.Literal` with :py:class:`ShExJ.objectLiteral` """
    return str(v1.value) == str(v2.value) and \
           (v2.language is None or v1.language == v2.language) and \
           (v2.type is None or uriref_matches_iriref(v1.datatype, v2.type))