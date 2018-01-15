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
from typing import Optional, Union, Tuple

from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p5_2_validation_definition import isValid
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import FixedShapeMap, ShapeAssociation
from pyshex.utils.schema_loader import SchemaLoader
from pyshex.shape_expressions_language.p5_context import Context
from rdflib import Graph, URIRef


def evaluate(g: Graph(),
             schema: Union[str, ShExJ.Schema],
             focus: Union[str, URIRef],
             start: Optional[Union[str, URIRef]]=None,
             debug_trace: bool = False) -> Tuple[bool, Optional[str]]:
    """ Evaluate focus node `focus` in graph `g` against shape `shape` in ShEx schema `schema`

    :param g: Graph containing RDF
    :param schema: ShEx Schema -- if str, it will be parsed
    :param focus: focus node in g
    :param start: Starting shape.  If omitted, the Schema start shape is used
    :return: None if success or failure reason if failure
    """
    if isinstance(schema, str):
        schema = SchemaLoader().loads(schema)
    if schema is None:
        return False, "Error parsing schema"
    if isinstance(focus, str):
        focus = URIRef(focus)
    if start is None:
        start = str(schema.start) if schema.start else None
    if start is None:
        return False, "No starting shape"
    cntxt = Context(g, schema)
    cntxt.debug_context.trace_satisfies = cntxt.debug_context.trace_matches = \
        cntxt.debug_context.trace_nodeSatisfies = debug_trace
    map_ = FixedShapeMap()
    map_.add(ShapeAssociation(focus, ShExJ.IRIREF(str(start))))
    test_result = isValid(cntxt, map_)
    return test_result, None
