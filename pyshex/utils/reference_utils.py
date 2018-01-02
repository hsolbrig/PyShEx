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
from typing import NamedTuple, Optional, List, Dict

from ShExJSG import ShExJ

from pyshex.utils.schema_utils import triple_reference_of


class referenceNode(NamedTuple):
    node: Optional[ShExJ.shapeExprLabel]
    refs: List["referenceNode"]


def reference_graph(S: ShExJ.Schema) -> List[referenceNode]:
    seen: Dict[ShExJ.shapeExprLabel, referenceNode] = {}
    nodes: List[referenceNode] = []

    if S.start is not None:
        nodes.append(shapeExprClosure(S, S.start, seen))
    for expr in S.shapes:
        if isinstance(expr, (ShExJ.ShapeAnd, ShExJ.ShapeOr)):
            nodes += [shapeExprClosure(S, el, seen) for el in expr.shapeExprs]
    return nodes


def shapeExprClosure(S: ShExJ.Schema, node: ShExJ.shapeExpr, seen: Dict[ShExJ.shapeExprLabel, referenceNode]) \
        -> referenceNode:
    """
    The shapeExpr closure of a shapeExpr SE includes every shape S that appears directly or by shapeExprRef in

    * ShapeAnd.shapeExprs or the shapeExpr closure of ShapeAnd.shapeExprs or
    * ShapeOr.shapeExprs or the shapeExpr closure of ShapeOr.shapeExprs or
    * ShapeNot.shapeExpr or the shapeExpr closure of ShapeNot.shapeExpr.
    """
    if node.id is not None and node.id in seen:
        return seen[node.id]
    if isinstance(node, (ShExJ.ShapeAnd, ShExJ.ShapeOr)):
        return referenceNode(node.id, [shapeExprClosure(S, e, seen) for e in node.shapeExprs])
    elif isinstance(node, ShExJ.ShapeNot):
        return referenceNode(node.id, [shapeExprClosure(S, node.shapeExpr, seen)])
    elif isinstance(node, ShExJ.shapeExprLabel)
        ref


def tripleExprClosure(schema: ShExJ.Schema, TE: ShExJ.tripleExpr, seen: Dict[ShExJ.shapeExprLabel, referenceNode])
    -> List[referenceNode]:
    """
    The tripleExpr closure of a tripleExpr TE includes every TripleConstraint TC that appears directly or by
     tripleExprRef in

    * EachOf.tripleExprs or the closure of EachOf.tripleExprs or
    * OneOf.tripleExprs or the closure of OneOf.tripleExprs.
    """
    rval: List[referenceNode] = []
    if isinstance(TE, (ShExJ.EachOf, ShExJ.OneOf)):
        for expr in TE.expressions:
            rval += tripleExprClosure(expr, seen)
    elif isinstance(TE, ShExJ.TripleConstraint):
        if TE.valueExpr:
            rval.append(shapeExprClosure(TE.valueExpr, seen))
    elif isinstance(TE, ShExJ.tripleExprLabel):
        tr = triple_reference_of(schema, TE)
        if tr is not None:
            rval += tripleExprClosure(schema, tr, seen)
