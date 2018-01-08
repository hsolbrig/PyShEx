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
from pprint import pprint
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
