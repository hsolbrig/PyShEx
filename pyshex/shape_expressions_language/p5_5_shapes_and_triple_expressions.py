""" Implementation of `5.5 Shapes and Triple Expressions <http://shex.io/shex-semantics/#shapes-and-TEs>`_"""

from typing import List, Optional, Union

from ShExJSG import ShExJ
from pyjsg.jsglib.jsg import isinstance_
from rdflib import URIRef

from pyshex.shape_expressions_language.p3_terminology import neigh, arcsOut
from pyshex.shape_expressions_language.p5_7_semantic_actions import semActsSatisfied
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.utils.debug_utils import satisfies_wrapper, matches_wrapper, remainder_wrapper
from pyshex.utils.partitions import partition_t, partition_2
from pyshex.utils.schema_utils import predicates_in_expression
from pyshex.utils.value_set_utils import uriref_matches_iriref, iriref_to_uriref


@satisfies_wrapper
def satisfiesShape(cntxt: Context, n: nodeSelector, S: ShExJ.Shape) -> bool:
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
    neighborhood = neigh(cntxt.graph, n)

    # Recursion detection.  If start_evaluating returns a boolean value, this is the assumed result of the shape
    # evaluation.  If it doesn't, evaluation is needed
    rslt = cntxt.start_evaluating(n, S)
    if rslt is None:
        # Evaluate the actual expression
        if S.expression:
            for matched, remainder in partition_2(neighborhood):
                if matches(cntxt, matched, S.expression) and valid_remainder(cntxt, n, remainder, S):
                    rslt = True
                    break
            rslt = rslt or False
        else:
            rslt = valid_remainder(cntxt, n, neighborhood, S)

        # If an assumption was made and the result doesn't match the assumption, switch directions and try again
        if not cntxt.done_evaluating(n, S, rslt):
            rslt = satisfiesShape(cntxt, n, S)
    return rslt


@remainder_wrapper
def valid_remainder(cntxt: Context, n: nodeSelector, remainder: RDFGraph, S: ShExJ.Shape) -> bool:
    """
    Let **outs** be the arcsOut in remainder: `outs = remainder ∩ arcsOut(G, n)`.

    Let **matchables** be the triples in outs whose predicate appears in a TripleConstraint in `expression`. If
    `expression` is absent, matchables = Ø (the empty set).

    * There is no triple in **matchables** which matches a TripleConstraint in expression

    * There is no triple in **matchables** whose predicate does not appear in extra.

    * closed is false or unmatchables is empty

    :param cntxt: evaluation context
    :param n: focus node
    :param remainder: non-matched triples
    :param S: Shape being evaluated
    :return: True if remainder is valid
    """
    # Let **outs** be the arcsOut in remainder: `outs = remainder ∩ arcsOut(G, n)`.
    outs = arcsOut(cntxt.graph, n).intersection(remainder)

    # predicates that in a TripleConstraint in `expression`
    predicates = predicates_in_expression(S, cntxt)

    # Let **matchables** be the triples in outs whose predicate appears in predicates. If
    # `expression` is absent, matchables = Ø (the empty set).
    matchables = RDFGraph(t for t in outs if str(t.p) in predicates)

    # There is no triple in **matchables** which matches a TripleConstraint in expression
    if matchables and S.expression is not None and matches(cntxt, matchables, S.expression):
        return False

    # There is no triple in **matchables** whose predicate does not appear in extra.
    extras = {iriref_to_uriref(e) for e in S.extra} if S.extra is not None else {}
    if any(t.p not in extras for t in matchables):
        return False

    # closed is false or unmatchables is empty.
    return not S.closed.val or not bool(outs - matchables)


@matches_wrapper
def matches(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExpr) -> bool:
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
    if isinstance_(expr, ShExJ.tripleExprLabel):
        expr = cntxt.tripleExprFor(expr)
    return matchesCardinality(cntxt, T, expr) and \
        (expr.semActs is None or semActsSatisfied(expr.semActs, cntxt))


@matches_wrapper
def matchesCardinality(cntxt: Context, T: RDFGraph, expr: Union[ShExJ.tripleExpr, ShExJ.tripleExprLabel]) -> bool:
    """ Evaluate cardinality expression
    expr has a cardinality of min and/or max not equal to 1, where a max of -1 is treated as unbounded, and
    T can be partitioned into k subsets T1, T2,…Tk such that min ≤ k ≤ max and for each Tn,
    matches(Tn, expr, m) by the remaining rules in this list.
    """
    # Set the cardinatlity defaults
    min_ = expr.min.val if expr.min.val is not None else 1
    max_ = expr.max.val if expr.max.val is not None else -1

    if len(T) < (min_):
        return False
    for partition in _partitions(T, min_, max_):
        if all(matchesExpr(cntxt, entry, expr) for entry in partition):
            return True
    return expr.min.val == 0


def _partitions(T: RDFGraph, min_: Optional[int], max_: Optional[int]) -> List[List[RDFGraph]]:
    if max_ == 1:
        yield [T]
    for k in range(min_, (max(len(T), min_) if max_ == -1 else max_)+1):
        for partition in partition_t(T, k):
            yield partition


@matches_wrapper
def matchesExpr(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExpr) -> bool:
    """ Evaluate the expression

    """
    if isinstance(expr, ShExJ.OneOf):
        return matchesOneOf(cntxt, T, expr)
    elif isinstance(expr, ShExJ.EachOf):
        return matchesEachOf(cntxt, T, expr)
    elif isinstance(expr, ShExJ.TripleConstraint):
        return matchesTripleConstraint(cntxt, T, expr)
    elif isinstance(expr, ShExJ.tripleExprLabel):
        return matchesTripleExprRef(cntxt, T, expr)
    else:
        raise Exception("Unknown expression")


@matches_wrapper
def matchesOneOf(cntxt: Context, T: RDFGraph, expr: ShExJ.OneOf) -> bool:
    """
    expr is a OneOf and there is some shape expression se2 in shapeExprs such that a matches(T, se2, m).
    :param T:
    :param expr:
    :param cntxt:
    :return:
    """
    return any(matches(cntxt, T, e) for e in expr.expressions)


@matches_wrapper
def matchesEachOf(cntxt: Context, T: RDFGraph, expr: ShExJ.EachOf) -> bool:
    """ expr is an EachOf and there is some partition of T into T1, T2,… such that for every expression
     expr1, expr2,… in shapeExprs, matches(Tn, exprn, m).
     """
    for partition in _partitions(T, len(expr.expressions), len(expr.expressions)):
        # TODO: debug
        # for t, e in zip(partition, expr.expressions):
        #     print(f"{[str(e) for e in t]} matches({e.predicate, type(e)})")
        if all(matches(cntxt, t, e) for t, e in zip(partition, expr.expressions)):
            return True
    return False


@matches_wrapper
def matchesTripleConstraint(cntxt: Context, T: RDFGraph, expr: ShExJ.TripleConstraint) -> bool:
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
            # TODO: debug
            # print(f"\t{t.p}=={expr.predicate}?")
            if uriref_matches_iriref(t.p, expr.predicate):
                value = t.s if expr.inverse.val else t.o
                # TODO: debug
                # print(f"\tsatisfies({value}, {type(expr.valueExpr)}")
                if expr.valueExpr is None or satisfies(cntxt, value, expr.valueExpr):
                    return True
    return False


@matches_wrapper
def matchesTripleExprRef(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExprLabel) -> bool:
    """
    expr is an tripleExprRef and satisfies(value, tripleExprWithId(tripleExprRef), G, m).
    The tripleExprWithId function is defined in Triple Expression Reference Requirement below.
    """
    return matchesTripleConstraint(cntxt, T, cntxt.tripleExprFor(expr))
