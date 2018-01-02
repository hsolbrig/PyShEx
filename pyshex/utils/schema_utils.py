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
from typing import Optional

from ShExJSG import ShExJ

from pyshex.shapemap_structure_and_language.p3_shapemap_structure import START, shapeLabel


def reference_of(schema: ShExJ.Schema, selector: shapeLabel) -> Optional[ShExJ.shapeExpr]:
    """ Return the shape expression in the schema referenced by selector, if any

    :param schema:
    :param selector:
    :return:
    """
    if isinstance(selector, START):
        return schema.start
    for expr in schema.shapes:
        if not isinstance(expr, ShExJ.ShapeExternal) and expr.id == selector:
            return expr
    return schema.start if schema.start is not None and schema.start.id == selector else None


def triple_reference_of(schema: ShExJ.Schema, label: ShExJ.tripleExprLabel) -> Optional[ShExJ.tripleExpr]:
    """ Search for the label in a Schema """
    te: Optional[ShExJ.tripleExpr] = None
    if schema.start is not None:
        te = triple_in_shape(schema, schema.start, label)
    if te is None:
        for shapeExpr in schema.shapes:
            te = triple_in_shape(schema, shapeExpr, label)
            if te:
                break
    return te


def triple_in_shape(schema: ShExJ.Schema, expr: ShExJ.shapeExpr, label: ShExJ.tripleExprLabel) \
        -> Optional[ShExJ.tripleExpr]:
    """ Search for the label in a shape expression """
    te = None
    if isinstance(expr, (ShExJ.ShapeOr, ShExJ.ShapeAnd)):
        for expr2 in expr.shapeExprs:
            te = triple_in_shape(schema, expr2, label)
            if te is not None:
                break
    elif isinstance(expr, ShExJ.ShapeNot):
        te = triple_in_shape(schema, expr.shapeExpr, label)
    elif isinstance(expr, ShExJ.shapeExprLabel):
        se = reference_of(schema, expr)
        if se is not None:
            te = triple_in_shape(schema, se, label)
    return te
