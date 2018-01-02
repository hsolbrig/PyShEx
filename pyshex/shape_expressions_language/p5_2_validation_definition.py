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
from turtledemo.planet_and_moon import G
from typing import List, Tuple

from ShExJSG import ShExJ
from rdflib import Graph

from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector, shapeLabel, QueryShapeMap

""" Implementation of `5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_
"""


def isValid(cntxt: Context, m: QueryShapeMap) -> bool:
    """`5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_

    The expression isValid(G, m) indicates that for every nodeSelector/shapeLabel pair (n, s) in m, s has a
        corresponding shape expression se and satisfies(n, se, G, m). satisfies is defined below for each form
        of shape expression
    :param cntxt: evaluation context - includes graph and schema
    :param m: list of NodeShape pairs to test
    :return:
    """
    return all(s in cntxt.schema.shapes and satisfies(n, cntxt.schema.shapes[s], cntxt) for n, s in m)
