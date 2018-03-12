""" Implementation of `5.3 Shape Expressions <http://shex.io/shex-semantics/#node-constraint-semantics>`_ """

from ShExJSG import ShExJ
from pyjsg.jsglib.jsg import isinstance_

from pyshex.shape_expressions_language.p5_4_node_constraints import satisfies2
from pyshex.shape_expressions_language.p5_5_shapes_and_triple_expressions import satisfiesShape
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.utils.debug_utils import satisfies_wrapper


@satisfies_wrapper
def satisfies(cntxt: Context, n: nodeSelector, se: ShExJ.shapeExpr) -> bool:
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

          .. note:: Where is the documentation on recursion?  All I can find is
           `5.9.4 Recursion Example <http://shex.io/shex-semantics/#example-recursion>`_
          """
    c = cntxt.debug_context
    if c.trace_satisfies:
        c.splus()
        print(f"--> Satisfies {c.d()}: "
              f"{n} {str(se) if isinstance_(se, ShExJ.shapeExprLabel) else 'type: ' + str(type(se))}")
    if isinstance(se, ShExJ.NodeConstraint):
        rval = satisfies2(cntxt, n, se)
    elif isinstance(se, ShExJ.Shape):
        rval = satisfiesShape(cntxt, n, se)
    elif isinstance(se, ShExJ.ShapeOr):
        rval = satisifesShapeOr(cntxt, n, se)
    elif isinstance(se, ShExJ.ShapeAnd):
        rval = satisfiesShapeAnd(cntxt, n, se)
    elif isinstance(se, ShExJ.ShapeNot):
        rval = satisfiesShapeNot(cntxt, n, se)
    elif isinstance(se, ShExJ.ShapeExternal):
        rval = satisfiesExternal(cntxt, n, se)
    elif isinstance_(se, ShExJ.shapeExprLabel):
        rval = satisfiesShapeExprRef(cntxt, n, se)
    else:
        raise NotImplementedError(f"Unrecognized shapeExpr: {type(se)}")
    if c.trace_satisfies:
        print(f"<-- Satisfies {c.d()} {rval}")
        c.sminus()
    return rval


def notSatisfies(cntxt: Context, n: nodeSelector, se: ShExJ.shapeExpr) -> bool:
    return not satisfies(cntxt, n, se)


def satisifesShapeOr(cntxt: Context, n: nodeSelector, se: ShExJ.ShapeOr) -> bool:
    """ Se is a ShapeOr and there is some shape expression se2 in shapeExprs such that satisfies(n, se2, G, m). """
    return any(satisfies(cntxt, n, se2) for se2 in se.shapeExprs)


def satisfiesShapeAnd(cntxt: Context, n: nodeSelector, se: ShExJ.ShapeAnd) -> bool:
    """ Se is a ShapeAnd and for every shape expression se2 in shapeExprs, satisfies(n, se2, G, m) """
    return all(satisfies(cntxt, n, se2) for se2 in se.shapeExprs)


def satisfiesShapeNot(cntxt: Context, n: nodeSelector, se: ShExJ.ShapeNot) -> bool:
    """ Se is a ShapeNot and for the shape expression se2 at shapeExpr, notSatisfies(n, se2, G, m) """
    return not satisfies(cntxt, n, se.shapeExpr)


def satisfiesExternal(cntxt: Context, n: nodeSelector, se: ShExJ.ShapeExternal) -> bool:
    """ Se is a ShapeExternal and implementation-specific mechansims not defined in this specification indicate
     success.
     """
    extern_shape = cntxt.external_shape_for(se.id)
    return extern_shape is not None and satisfies(cntxt, n, extern_shape)


def satisfiesShapeExprRef(cntxt: Context, n: nodeSelector, se: ShExJ.shapeExprLabel) -> bool:
    """ Se is a shapeExprRef and there exists in the schema a shape expression se2 with that id
     and satisfies(n, se2, G, m).
     """
    for shape in cntxt.schema.shapes:
        if shape.id == se:
            return satisfies(cntxt, n, shape)
    c = cntxt.debug_context
    if c.trace_satisfies:
        print(c.i(1, f"***** Shape {se} not found"))
    return False
