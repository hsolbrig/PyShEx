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
from typing import Set, List

from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p3_terminology import neigh
from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
from pyshex.shape_expressions_language.p5_7_semantic_actions import semActsSatisfied
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFTriple
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.utils.partitions import partition_t
from pyshex.utils.value_set_utils import uriref_matches_iriref


def satisfiesShape(n: nodeSelector, S: ShExJ.Shape, cntxt: Context) -> bool:
    """ `5.5.2 Semantics <http://shex.io/shex-semantics/#triple-expressions-semantics>`_

    For a node `n`, shape `S`, graph `G`, and shapeMap `m`, `satisfies(n, S, G, m)` if and only if:

    * `neigh(G, n)` can be partitioned into two sets matched and remainder such that
      `matches(matched, expression, m)`. If expression is absent, remainder = `neigh(G, n)`.

       Let **outs** be the arcsOut in remainder: outs = remainder ∩ arcsOut(G, n).

       Let **matchables** be the triples in outs whose predicate appears in a TripleConstraint in expression. If
       expression is absent, matchables = Ø (the empty set).

       The complexity of partitioning is described briefly in the ShEx2 Primer.
    * There is no triple in **matchables** which matches a TripleConstraint in expression. ::

      Let **unmatchables** be the triples in outs which are not in matchables. matchables ∪ unmatchables = outs.
    * There is no triple in matchables whose predicate does not appear in extra.
    * closed is false or unmatchables is empty.
    """
    matched, remainder = partition(neigh(cntxt.graph, n), S.expression)
    return False


def matches(T: Set[RDFTriple], expr: ShExJ.tripleExpr, cntxt: Context) -> bool:
    """
    **matches**: asserts that a triple expression is matched by a set of triples that come from the neighbourhood of a
    node in an RDF graph. The expression `matches(T, expr, m)` indicates that a set of triples `T` can satisfy these
    rules:

    * expr has semActs and `matches(T, expr, m)` by the remaining rules in this list and the evaluation
      of semActs succeeds according to the section below on Semantic Actions.
    * expr has a cardinality of min and/or max not equal to 1, where a max of -1 is treated as unbounded, and T
      can be partitioned into k subsets T1, T2,…Tk such that min ≤ k ≤ max and for each Tn,
      `matches(Tn, expr, m)` by the remaining rules in this list.
    * expr is a OneOf and there is some shape expression se2 in shapeExprs such that a matches(T, se2, m).
    * expr is an EachOf and there is some partition of T into T1, T2,… such that for every expression
      expr1, expr2,… in shapeExprs, matches(Tn, exprn, m).
    * expr is a TripleConstraint and:
        * T is a set of one triple. Let t be the soul triple in T.
        * t's predicate equals expr's predicate. Let value be t's subject if inverse is true, else t's object.
        * if inverse is true, t is in arcsIn, else t is in arcsOut.
        * either
            * expr has no valueExpr
            * or `satisfies(value, valueExpr, G, m).

    :param T:
    :param expr:
    :param cntxt:
    :return:
    """
    # if isinstance(expr, ShExJ.OneOf):
    #     return any(matches(T, shapeExpr, m) for shapeExpr in expr.expressions)
    # elif isinstance(expr, ShExJ.EachOf):
    #     for Ts in partitions(T, len(expr.expressions)):
    #         for
    return matchesCardinality(T, expr, cntxt) and (semActsSatisfied(expr.semActs) if expr.semActs is not None else True)


def matchesCardinality(T: Set[RDFTriple], expr: ShExJ.tripleExpr, cntxt: Context) -> bool:
    """ Evaluate cardinality expression
    expr has a cardinality of min and/or max not equal to 1, where a max of -1 is treated as unbounded, and
    T can be partitioned into k subsets T1, T2,…Tk such that min ≤ k ≤ max and for each Tn,
    matches(Tn, expr, m) by the remaining rules in this list.
    """
    return any(all(matchesExpr(t, expr, cntxt) for t in partition) for partition in _partitions(T, expr.min, expr.max))


def _partitions(T: Set[RDFTriple], min_: int, max_: int) -> List[List[Set[RDFTriple]]]:
    ts = sorted(List(T))
    if max_ == 1:
        return [[T]]
    for k in range(min_, min(max_, len(T))):
        for partition in partition_t(ts, k):
            yield next(partition)


def matchesExpr(T: Set[RDFTriple], expr: ShExJ.tripleExpr, cntxt: Context) -> bool:
    """ Evaluate the expression

    """
    if isinstance(expr, ShExJ.OneOf):
        return matchesOneOf(T, expr, cntxt)
    elif isinstance(expr, ShExJ.EachOf):
        return matchesEachOf(T, expr, cntxt)
    elif isinstance(expr, ShExJ.TripleConstraint):
        return matchesTripleConstraint(T, expr, cntxt)
    elif isinstance(expr, ShExJ.tripleExprLabel):
        return False
    else:
        raise Exception("Unknown expression")


def matchesOneOf(T: Set[RDFTriple], expr: ShExJ.OneOf, cntxt: Context) -> bool:
    """
    expr is a OneOf and there is some shape expression se2 in shapeExprs such that a matches(T, se2, m).
    :param T:
    :param expr:
    :param cntxt:
    :return:
    """
    return any(matches(T, e, cntxt) for e in expr.expressions)


def matchesEachOf(T: Set[RDFTriple], expr: ShExJ.EachOf, cntxt: Context) -> bool:
    """ expr is an EachOf and there is some partition of T into T1, T2,… such that for every expression
     expr1, expr2,… in shapeExprs, matches(Tn, exprn, m).
     """
    for partition in _partitions(T, len(expr.expressions), len(expr.expressions)):
        if all(matches(t, e, cntxt) for t, e in zip(partition, expr.expressions)):
            return True
    return False


def matchesTripleConstraint(T: Set[RDFTriple], expr: ShExJ.TripleConstraint, cntxt: Context) -> bool:
    """
    expr is a TripleConstraint and:

    * T is a set of one triple.
    * Let t be the soul triple in T.
    * t's predicate equals expr's predicate.
      Let value be t's subject if inverse is true, else t's object.
    * if inverse is true, t is in arcsIn, else t is in arcsOut.

    """
    if len(T) == 1:
        for t in T:
            if uriref_matches_iriref(t.predicate, expr.predicate):
                value = t.subject if expr.inverse else t.object
                if expr.valueExpr is None:
                    return True
                else:
                    satisfies(value, expr.valueExpr, cntxt)


def matchesTripleExprRef(T: Set[RDFTriple], expr: ShExJ.TripleConstraint, cntxt: Context) -> bool:
    """
    expr is an tripleExprRef and satisfies(value, tripleExprWithId(tripleExprRef), G, m).
    The tripleExprWithId function is defined in Triple Expression Reference Requirement below.
    """