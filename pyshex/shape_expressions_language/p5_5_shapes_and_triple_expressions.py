""" Implementation of `5.5 Shapes and Triple Expressions <http://shex.io/shex-semantics/#shapes-and-TEs>`_"""

from typing import Set, List, Optional

from ShExJSG import ShExJ

from pyshex.shape_expressions_language.p3_terminology import neigh, arcsOut
from pyshex.shape_expressions_language.p5_7_semantic_actions import semActsSatisfied
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFTriple
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.utils.partitions import partition_t, partition_2
from pyshex.utils.schema_utils import predicates_in_expression
from pyshex.utils.value_set_utils import uriref_matches_iriref


def satisfiesShape(n: nodeSelector, S: ShExJ.Shape, cntxt: Context) -> bool:
    """ `5.5.2 Semantics <http://shex.io/shex-semantics/#triple-expressions-semantics>`_

    For a node `n`, shape `S`, graph `G`, and shapeMap `m`, `satisfies(n, S, G, m)` if and only if:

    * `neigh(G, n)` can be partitioned into two sets matched and remainder such that
      `matches(matched, expression, m)`. If expression is absent, remainder = `neigh(G, n)`.

    :param n: focus node
    :param S: Shape to be satisfied
    :param cntxt: Evaluation context
    :return: true iff `satisfies(n, S, cntxt)`
    """
    # This is an extremely inefficient way to do this, as we could actually be quite clever about how to approach this,
    # but we are first implementing this literally
    neighborhood = list(neigh(cntxt.graph, n))

    if S.expression:
        for matched, remainder in partition_2(neighborhood):
            print(f"--> ({len(matched)}, {len(remainder)})")
            if matches(matched, S.expression, cntxt) and valid_remainder(n, remainder, S, cntxt) or \
                    matches(remainder, S.expression, cntxt) and valid_remainder(n, matched, S, cntxt):
                return True
        return False
    else:
        return valid_remainder(n, neighborhood, S, cntxt)


def valid_remainder(n: nodeSelector, remainder: List[RDFTriple], S: ShExJ.Shape, cntxt: Context) -> bool:
    """
    Let **outs** be the arcsOut in remainder: `outs = remainder ∩ arcsOut(G, n)`.

    Let **matchables** be the triples in outs whose predicate appears in a TripleConstraint in `expression`. If
    `expression` is absent, matchables = Ø (the empty set).

    * There is no triple in **matchables** which matches a TripleConstraint in expression

    * There is no triple in **matchables** whose predicate does not appear in extra.

    * closed is false or unmatchables is empty

    :param n: focus node
    :param remainder: non-matched triples
    :param S: Shape being evaluated
    :param cntxt: evaluation context
    :return: True if remainder is valid
    """
    # Let **outs** be the arcsOut in remainder: `outs = remainder ∩ arcsOut(G, n)`.
    outs = arcsOut(cntxt.graph, n).intersection(remainder)

    # predicates that in a TripleConstraint in `expression`
    predicates = predicates_in_expression(S.expression, cntxt) if S.expression is not None else []

    # Let **matchables** be the triples in outs whose predicate appears in predicates. If
    # `expression` is absent, matchables = Ø (the empty set).
    matchables = {t for t in outs if str(t.predicate) in predicates}

    # There is no triple in **matchables** which matches a TripleConstraint in expression
    if matchables and S.expression is not None and matches(matchables, S.expression, cntxt):
        return False

    # There is no triple in **matchables** whose predicate does not appear in extra.
    extras = S.extra if S.extra is not None else {}
    if any(t.predicate not in extras for t in matchables):
        return False

    # closed is false or unmatchables is empty.
    return not S.closed.val or outs - matchables


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
        * if inverse is true, t is in arcsIn, else t is in `arcsOut`.
        * either
            * expr has no valueExpr
            * or `satisfies(value, valueExpr, G, m).
    """
    return matchesCardinality(T, expr, cntxt) and \
        (expr.semActs is None or semActsSatisfied(expr.semActs, cntxt))


def matchesCardinality(T: Set[RDFTriple], expr: ShExJ.tripleExpr, cntxt: Context) -> bool:
    """ Evaluate cardinality expression
    expr has a cardinality of min and/or max not equal to 1, where a max of -1 is treated as unbounded, and
    T can be partitioned into k subsets T1, T2,…Tk such that min ≤ k ≤ max and for each Tn,
    matches(Tn, expr, m) by the remaining rules in this list.
    """
    if len(T) < (expr.min.val if expr.min.val is not None else 1):
        return False
    for partition in _partitions(T, expr.min.val, expr.max.val):
        if all(matchesExpr(entry, expr, cntxt) for entry in partition):
            return True
    return expr.min.val == 0


def _partitions(T: Set[RDFTriple], min_: Optional[int], max_: Optional[int]) -> List[List[Set[RDFTriple]]]:
    if min_ is None:
        min_ = 1
    if max_ is None:
        max_ = 1
    if max_ == 1:
        yield [T]
    ts = sorted(list(T))
    for k in range(min_, (len(T) if max_ == -1 else min(max_, len(T))) + 1):
        for partition in partition_t(ts, k):
            yield partition


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
    from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
    if len(T) == 1:
        for t in T:
            if uriref_matches_iriref(t.predicate, expr.predicate):
                value = t.subject if expr.inverse.val else t.object
                if expr.valueExpr is None or satisfies(cntxt, value, expr.valueExpr):
                    return True
    return False



def matchesTripleExprRef(T: Set[RDFTriple], expr: ShExJ.tripleExprLabel, cntxt: Context) -> bool:
    """
    expr is an tripleExprRef and satisfies(value, tripleExprWithId(tripleExprRef), G, m).
    The tripleExprWithId function is defined in Triple Expression Reference Requirement below.
    """
    return matchesTripleConstraint(T, cntxt.tripleExprFor(expr), cntxt)
