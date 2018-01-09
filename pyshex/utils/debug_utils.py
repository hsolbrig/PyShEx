from typing import Callable, Any, Set

from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFTriple
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector


def satisfies_wrapper(f: Callable[[Context, nodeSelector, ShExJ.shapeExpr], bool]) -> Callable:
    def w(cntxt: Context, n: nodeSelector, s: ShExJ.shapeExpr) -> bool:
        if cntxt.debug_context.trace_satisfies:
            cntxt.debug_context.trace_indent += 1
            print(f"{'   '*cntxt.debug_context.trace_indent}(C) {f.__name__}({n}, {type(s)})")
        rval = f(cntxt, n, s)
        if cntxt.debug_context.trace_satisfies:
            print(f"{'   '*cntxt.debug_context.trace_indent}(R) {f.__name__}({n}, {type(s)}) -> {rval}")
            cntxt.debug_context.trace_indent -= 1
        return rval
    return w


def nodeSatisfies_wrapper(f: Callable[[Context, nodeSelector, ShExJ.NodeConstraint], bool]) -> Callable:
    def w(cntxt: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
        if cntxt.debug_context.trace_nodeSatisfies:
            cntxt.debug_context.trace_indent += 1
            print(f"{'   '*cntxt.debug_context.trace_indent}(C) {f.__name__}({n}, {type(nc)})")
        rval = f(cntxt, n, nc)
        if cntxt.debug_context.trace_satisfies:
            print(f"{'   '*cntxt.debug_context.trace_indent}(R) {f.__name__}({n}, {type(nc)}) -> {rval}")
            cntxt.debug_context.trace_indent -= 1
        return rval
    return w


def matches_wrapper(f: Callable[[Context, Set[RDFTriple], ShExJ.tripleExpr], bool]) -> Callable:
    def w(cntxt: Context, T: Set[RDFTriple], te: ShExJ.tripleExpr) -> bool:
        if cntxt.debug_context.trace_matches:
            cntxt.debug_context.trace_indent += 1
            print(f"{'   '*cntxt.debug_context.trace_indent}(C) {f.__name__}({T}, )")
        rval = f(cntxt, T, te)
        if cntxt.debug_context.trace_matches:
            print(f"{'   '*cntxt.debug_context.trace_indent}(R) {f.__name__}(T, ) -> {rval}")
            cntxt.debug_context.trace_indent -= 1
        return rval
    return w


def basic_function_wrapper(f: Callable[[Context, Any], bool]) -> Callable:
    def w(cntxt: Context, *args, **kwargs):
        if cntxt.debug_context.trace_satisfies or cntxt.debug_context.trace_nodeSatisfies:
            cntxt.debug_context.trace_indent += 1
            print(f"{'   '*cntxt.debug_context.trace_indent}(C) {f.__name__}")
        rval = f(cntxt, *args, **kwargs)
        if cntxt.debug_context.trace_satisfies or cntxt.debug_context.trace_nodeSatisfies:
            print(f"{'   '*cntxt.debug_context.trace_indent}(R) {f.__name__} -> {rval}")
            cntxt.debug_context.trace_indent -= 1
        return rval
    return w
