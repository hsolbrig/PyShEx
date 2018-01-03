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
from typing import Optional, Union, List

from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF

from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import START, shapeLabel


def reference_of(selector: shapeLabel, cntxt: Union[Context, ShExJ.Schema] ) -> Optional[ShExJ.shapeExpr]:
    """ Return the shape expression in the schema referenced by selector, if any

    :param cntxt: Context node or ShEx Schema
    :param selector: identifier of element to select within the schema
    :return:
    """
    schema = cntxt.schema if isinstance(cntxt, Context) else cntxt
    if isinstance(selector, START):
        return schema.start
    for expr in schema.shapes:
        if not isinstance(expr, ShExJ.ShapeExternal) and expr.id == selector:
            return expr
    return schema.start if schema.start is not None and schema.start.id == selector else None


def triple_reference_of(label: ShExJ.tripleExprLabel, cntxt: Context) -> Optional[ShExJ.tripleExpr]:
    """ Search for the label in a Schema """
    te: Optional[ShExJ.tripleExpr] = None
    if cntxt.schema.start is not None:
        te = triple_in_shape(cntxt.schema.start, label, cntxt)
    if te is None:
        for shapeExpr in cntxt.schema.shapes:
            te = triple_in_shape(shapeExpr, label, cntxt)
            if te:
                break
    return te


def triple_in_shape(expr: ShExJ.shapeExpr, label: ShExJ.tripleExprLabel, cntxt: Context) \
        -> Optional[ShExJ.tripleExpr]:
    """ Search for the label in a shape expression """
    te = None
    if isinstance(expr, (ShExJ.ShapeOr, ShExJ.ShapeAnd)):
        for expr2 in expr.shapeExprs:
            te = triple_in_shape(expr2, label, cntxt)
            if te is not None:
                break
    elif isinstance(expr, ShExJ.ShapeNot):
        te = triple_in_shape(expr.shapeExpr, label, cntxt)
    elif isinstance(expr, ShExJ.shapeExprLabel):
        se = reference_of(expr, cntxt)
        if se is not None:
            te = triple_in_shape(se, label, cntxt)
    return te


def predicates_in_expression(expression: ShExJ.shapeExpr, cntxt: Context) -> List[IRIREF]:
    """ Return the set of predicates that "appears in a TripleConstraint in an expression
    
    See: `5.5.2 Semantics <http://shex.io/shex-semantics/#triple-expressions-semantics>`_ for details

    :param expression: Expression to scan for predicates
    :param cntxt: Context of evaluation
    "return: List of predicates
    """
    predicates: List[IRIREF] = []

    def predicate_finder(predicates: List[IRIREF], expr: ShExJ.shapeExpr, cntxt: Context) -> None:
        if isinstance(expr, ShExJ.Shape) and expr.expression is not None:
            if isinstance(expr.expression, ShExJ.TripleConstraint):
                predicates.append(expr.expression.predicate)
            elif isinstance(expr.expression, ShExJ.tripleExprLabel):
                predicates.append(cntxt.tripleExprFor(expr.expression).predicate)

    cntxt.visit_shapes(expression, predicate_finder, predicates)
    return predicates
