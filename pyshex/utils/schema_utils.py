from typing import Optional, Union, List

from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF
from pyjsg.jsglib.jsg import isinstance_
from rdflib import URIRef

from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import START, shapeLabel


def reference_of(selector: shapeLabel, cntxt: Union[Context, ShExJ.Schema] ) -> Optional[ShExJ.shapeExpr]:
    """ Return the shape expression in the schema referenced by selector, if any

    :param cntxt: Context node or ShEx Schema
    :param selector: identifier of element to select within the schema
    :return:
    """
    schema = cntxt.schema if isinstance(cntxt, Context) else cntxt
    if selector is START:
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
            elif isinstance_(expr.expression, ShExJ.tripleExprLabel):
                predicates.append(cntxt.tripleExprFor(expr.expression).predicate)

    cntxt.visit_shapes(expression, predicate_finder, predicates, follow_inner_shapes=False)
    return predicates
