
"""
Context for evaluation engine -- carries all of the global variables (schema, graph, etc.)

We might fold the various routines inside context and replace "cntxt: Context" with "self", but we will have to see.

"""
from typing import Dict, Any, Callable, Optional

from ShExJSG import ShExJ
from ShExJSG.ShExJ import Schema
from rdflib import Graph


class _VisitorCenter:
    """ A visitor context -- couldn't resist calling it Visitor Center, however... it is python, you know """
    def __init__(self, f: Callable[[Any, ShExJ.shapeExpr, "Context"], None], arg_cntxt: Any) \
            -> None:
        self.f = f
        self.arg_cntxt = arg_cntxt
        self._seen_shapes = []
        self._visiting_shapes = []
        self._seen_tes = []
        self._visiting_tes = []

    def start_visiting_shape(self, id_: str) -> None:
        self._visiting_shapes.append(id_)

    def actively_visiting_shape(self, id_: str) -> bool:
        return id_ in self._visiting_shapes

    def done_visiting_shape(self, id_: str) -> None:
        self._visiting_shapes.remove(id_)
        self._seen_shapes.append(id_)

    def already_seen_shape(self, id_: str) -> bool:
        return id_ in self._seen_shapes

    def start_visiting_te(self, id_: str) -> None:
        self._visiting_tes.append(id_)

    def actively_visiting_te(self, id_: str) -> bool:
        return id_ in self._visiting_tes

    def done_visiting_te(self, id_: str) -> None:
        self._visiting_tes.remove(id_)
        self._seen_tes.append(id_)

    def already_seen_te(self, id_: str) -> bool:
        return id_ in self._seen_tes


class Context:
    """ Environment for ShExJ evaluation """
    def __init__(self, g: Optional[Graph], s: Schema):
        """
        Create a context consisting of an RDF Graph and a ShEx Schema and generate a identifier to
        item map.

        :param g: RDF graph
        :param s: ShExJ Schema instance
        """
        self.graph = g
        self.schema = s
        self.schema_id_map: Dict[ShExJ.shapeExprLabel, ShExJ.shapeExpr] = {}
        self.te_id_map: Dict[ShExJ.tripleExprLabel, ShExJ.tripleExpr] = {}
        if self.schema.start is not None:
            self._gen_schema_xref(self.schema.start)
        if self.schema.shapes is not None:
            for e in self.schema.shapes:
                self._gen_schema_xref(e)

    def _gen_schema_xref(self, expr: ShExJ.shapeExpr) -> None:
        """
        Generate the schema_id_map

        :param expr: root shape expression
        """
        if 'id' in expr and expr.id is not None:
            if expr.id in self.schema_id_map:
                return
            else:
                self.schema_id_map[expr.id] = expr
        if isinstance(expr, (ShExJ.ShapeOr, ShExJ.ShapeAnd)):
            for expr2 in expr.shapeExprs:
                self._gen_schema_xref(expr2)
        elif isinstance(expr, ShExJ.ShapeNot):
            self._gen_schema_xref(expr)
        elif isinstance(expr, ShExJ.Shape):
            if expr.expression is not None:
                self._gen_te_xref(expr.expression)

    def _gen_te_xref(self, expr: ShExJ.tripleExpr) -> None:
        """
        Generate the triple expression map (te_id_map)

        :param expr: root triple expression

        """
        if 'id' in expr and expr.id is not None:
            if expr.id in self.te_id_map:
                return
            else:
                self.te_id_map[expr.id] = expr
        if isinstance(expr, (ShExJ.OneOf, ShExJ.EachOf)):
            for expr2 in expr.expressions:
                self._gen_te_xref(expr2)
        elif isinstance(expr, ShExJ.TripleConstraint):
            if expr.valueExpr is not None:
                self._gen_schema_xref(expr.valueExpr)

    def tripleExprFor(self, id_: ShExJ.tripleExprLabel) -> ShExJ.tripleExpr:
        """ Return the triple expression that corresponds to id """
        return self.te_id_map[id_]

    def shapeExprFor(self, id_: ShExJ.shapeExprLabel) -> ShExJ.shapeExpr:
        """ Return the shape expression that corresponds to id """
        return self.schema_id_map[id_]

    def visit_shapes(self, expr: ShExJ.shapeExpr, f: Callable[[Any, ShExJ.shapeExpr, "Context"], None], arg_cntxt: Any,
                     visit_center: _VisitorCenter = None) -> None:
        """
        Visit expr and all of its "descendant" shapes.

        :param expr: root shape expression
        :param f: visitor function
        :param arg_cntxt: accompanying context for the visitor function
        :param visit_center: Recursive visit context.  (Not normally supplied on an external call)
        """
        if visit_center is None:
            visit_center = _VisitorCenter(f, arg_cntxt)
        has_id = 'id' in expr and expr.id is not None
        if not has_id or not (visit_center.already_seen_shape(expr.id) or visit_center.actively_visiting_shape(expr.id)):

            # Visit the root expression
            if has_id:
                visit_center.start_visiting_shape(expr.id)
            f(arg_cntxt, expr, self)

            # Traverse the expression and visit its components
            if isinstance(expr, (ShExJ.ShapeOr, ShExJ.ShapeAnd)):
                for expr2 in expr.shapeExprs:
                    self.visit_shapes(expr2, f, arg_cntxt, visit_center)
            elif isinstance(expr, ShExJ.ShapeNot):
                self.visit_shapes(expr.shapeExpr, f, arg_cntxt, visit_center)
            elif isinstance(expr, ShExJ.Shape):
                if expr.expression is not None:
                    self.visit_triple_expressions(expr.expression,
                                                  lambda ac, te, cntxt: self._visit_shape_te(te, visit_center),
                                                  arg_cntxt,
                                                  visit_center)
            elif ShExJ.isinstance_(expr, ShExJ.shapeExprLabel):
                if not visit_center.actively_visiting_shape(str(expr)):
                    visit_center.start_visiting_shape(str(expr))
                    self.visit_shapes(self.shapeExprFor(expr), f, arg_cntxt, visit_center)
                    visit_center.done_visiting_shape(str(expr))
            if has_id:
                visit_center.done_visiting_shape(expr.id)

    def visit_triple_expressions(self, expr: ShExJ.tripleExpr, f: Callable[[Any, ShExJ.tripleExpr, "Context"], None],
                                 arg_cntxt: Any, visit_center: _VisitorCenter=None) -> None:
        if visit_center is None:
            visit_center = _VisitorCenter(f, arg_cntxt)
        has_id = 'id' in expr and expr.id is not None
        if not has_id or visit_center.already_seen_te(expr.id):

            # Visit the root expression
            if has_id:
                visit_center.start_visiting_te(expr.id)
            f(arg_cntxt, expr, self)

            # Visit all of the references
            if isinstance(expr, (ShExJ.EachOf, ShExJ.OneOf)):
                for expr2 in expr.expressions:
                    self.visit_triple_expressions(expr2, f, arg_cntxt, visit_center)
            elif isinstance(expr, ShExJ.TripleConstraint):
                if expr.valueExpr is not None:
                    self.visit_triple_expressions(expr.valueExpr,
                                                  lambda ac, te, cntxt: self._visit_te_shape(te, visit_center),
                                                  arg_cntxt,
                                                  visit_center)
            elif ShExJ.isinstance_(expr, ShExJ.tripleExprLabel):
                if not visit_center.actively_visiting_shape(str(expr)):
                    visit_center.start_visiting_shape(str(expr))
                    self.visit_shapes(self.tripleExprFor(expr), f, arg_cntxt, visit_center)
                    visit_center.done_visiting_shape(str(expr))
            if has_id:
                visit_center.done_visiting_te(expr.id)

    def _visit_shape_te(self, te: ShExJ.tripleExpr, visit_center: _VisitorCenter) -> None:
        """
        Visit a triple expression that was reached through a shape. This, in turn, is used to visit additional shapes
        that are referenced by a TripleConstraint
        :param te: Triple expression reached through a Shape.expression
        :param visit_center: context used in shape visitor
        """
        if isinstance(te, ShExJ.TripleConstraint) and te.valueExpr is not None:
            visit_center.f(visit_center.arg_cntxt, te.valueExpr, self)

    def _visit_te_shape(self, shape: ShExJ.shapeExpr, visit_center: _VisitorCenter) -> None:
        """
        Visit a shape expression that was reached through a triple expression.  This, in turn, is used to visit
        additional triple expressions that are referenced by the Shape

        :param shape: Shape reached through triple expression traverse
        :param visit_center: context used in shape visitor
        """
        if isinstance(shape, ShExJ.Shape) and shape.expression is not None:
            visit_center.f(visit_center.arg_cntxt, shape.expression, self)
