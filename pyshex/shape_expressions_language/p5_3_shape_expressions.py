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
from rdflib import Graph

from pyshex.shape_expressions_language.p5_4_node_constraints import satisfies2
from pyshex.shape_expressions_language.p5_5_shapes_and_triple_expressions import satisfiesShape
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector, ShapeMap


def satisfies(n: nodeSelector, se: ShExJ.shapeExpr, cntxt: Context) -> bool:
    """ `5.3 Shape Expressions <http://shex.io/shex-semantics/#node-constraint-semantics>`_

          satisfies: The expression satisfies(n, se, G, m) indicates that a node n and graph G satisfy a shape
                      expression se with shapeMap m.

           satisfies(n, se, G, m) is true if and only if:

            * Se is a NodeConstraint and satisfies2(n, se) as described below in Node Constraints.
                      Note that testing if a node satisfies a node constraint does not require a graph or shapeMap.
            * Se is a Shape and satisfies(n, se) as defined below in Shapes and Triple Expressions.
            * Se is a ShapeOr and there is some shape expression se2 in shapeExprs such that
            satisfies(n, se2, G, m).
            * Se is a ShapeAnd and for every shape expression se2 in shapeExprs, satisfies(n, se2, G, m).
            * Se is a ShapeNot and for the shape expression se2 at shapeExpr, notSatisfies(n, se2, G, m).
            * Se is a ShapeExternal and implementation-specific mechansims not defined in this specification
            indicate success.
            * Se is a shapeExprRef and there exists in the schema a shape expression se2 with that id and
                      satisfies(n, se2, G, m).

          :param n: node to test for satisfaction
          :param se: shape expression to be tested against
          :param G:
          :param m:
          :return:
          """
    return (isinstance(se, ShExJ.NodeConstraint) and satisfies2(n, se)) or \
           (isinstance(se, ShExJ.Shape) and satisfiesShape(n, se, cntxt)) or \
           (isinstance(se, ShExJ.ShapeOr) and satisifesShapeOr(n, se, cntxt)) or \
           (isinstance(se, ShExJ.ShapeAnd) and satisfiesShapeAnd(n, se, cntxt)) or \
           (isinstance(se, ShExJ.ShapeNot) and satisfiesShapeNot(n, se,  cntxt)) or \
           (isinstance(se, ShExJ.ShapeExternal) and satisfiesExternal(n, se,  cntxt)) or \
           (isinstance(se, ShExJ.shapeExprLabel) and satisfiesShapeExprRef(n, se, cntxt))


def notSatisfies(n: nodeSelector, se: ShExJ.shapeExpr, cntxt: Context) -> bool:
    return not satisfies(n, se, cntxt)


def satisifesShapeOr(n: nodeSelector, se: ShExJ.ShapeOr, cntxt: Context) -> bool:
    """ Se is a ShapeOr and there is some shape expression se2 in shapeExprs such that satisfies(n, se2, G, m). """
    return any(satisfies(n, se2, cntxt) for se2 in se.shapeExprs)


def satisfiesShapeAnd(n: nodeSelector, se: ShExJ.ShapeAnd, G: Graph, cntxt: Context) -> bool:
    """ Se is a ShapeAnd and for every shape expression se2 in shapeExprs, satisfies(n, se2, G, m) """
    return all(satisfies(n, se2, cntxt) for se2 in se.shapeExprs)


def satisfiesShapeNot(n: nodeSelector, se: ShExJ.ShapeNot, G: Graph, cntxt: Context) -> bool:
    """ Se is a ShapeNot and for the shape expression se2 at shapeExpr, notSatisfies(n, se2, G, m) """
    return not satisfies(n, se.shapeExpr, cntxt)


def satisfiesExternal(n: nodeSelector, se: ShExJ.ShapeExternal, cntxt: Context) -> bool:
    """ Se is a ShapeExternal and implementation-specific mechansims not defined in this specification indicate
     success.
     """
    return False


def satisfiesShapeExprRef(n: nodeSelector, se: ShExJ.shapeExprLabel, cntxt: Context) -> bool:
    """ Se is a shapeExprRef and there exists in the schema a shape expression se2 with that id
     and satisfies(n, se2, G, m).
     """
    for shape in cntxt.schema.shapes:
        if shape.id == se:
            return satisfies(n, shape, cntxt)
    return False
