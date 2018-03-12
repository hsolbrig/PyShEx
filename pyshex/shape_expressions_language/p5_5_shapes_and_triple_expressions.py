""" Implementation of `5.5 Shapes and Triple Expressions <http://shex.io/shex-semantics/#shapes-and-TEs>`_"""

from typing import List, Optional, Union, Dict

from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF
from pyjsg.jsglib.jsg import isinstance_

from pyshex.shape_expressions_language.p3_terminology import neigh, arcsOut
from pyshex.shape_expressions_language.p5_7_semantic_actions import semActsSatisfied
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.utils.debug_utils import satisfies_wrapper, matches_wrapper, remainder_wrapper
from pyshex.utils.partitions import partition_t, partition_2
from pyshex.utils.schema_utils import predicates_in_expression, triple_constraints_in_expression
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
    predicates = predicates_in_expression(S, cntxt)
    matchables = RDFGraph([t for t in neighborhood if str(t.p) in predicates])
    non_matchables = RDFGraph([t for t in neighborhood if str(t.p) not in predicates])

    c = cntxt.debug_context
    if c.trace_satisfies:
        print(c.i(1, f"---> Satisfies shape {c.d()}"))
        print(c.i(2, f"subject: {n}"))
        print(c.i(2, "predicates:", sorted(str(p) for p in predicates)))
        print(c.i(2, "matchables:", sorted(str(m) for m in matchables)))
        print()

    if S.closed.val and len(non_matchables):
        if c.trace_satisfies:
            print(c.i(1, f"<--- Satisfies shape {c.d()} FAIL - {len(non_matchables)} non matchables on a closed shape"))
            print(c.i(2, "", non_matchables))
            print()
        return False

    if rslt is None:
        # Evaluate the actual expression.  Start assuming everything matches...
        if S.expression:
            if matches(cntxt, matchables, S.expression):
                rslt = True
            else:
                for matched, remainder in partition_2(matchables):
                    if len(remainder):
                        if c.trace_satisfies:
                            print(c.i(1, f"***** matched = {len(matched)} remainder = {len(remainder)}"))
                        if matches(cntxt, matched, S.expression) and valid_remainder(cntxt, n, remainder, S):
                            rslt = True
                            break
                rslt = rslt or False
        else:
            rslt = valid_remainder(cntxt, n, neighborhood, S)

        # If an assumption was made and the result doesn't match the assumption, switch directions and try again
        if not cntxt.done_evaluating(n, S, rslt):
            rslt = satisfiesShape(cntxt, n, S)
    if c.trace_satisfies:
        print(f"<--- Satisfies shape {c.d()} {rslt}")
    return rslt


@remainder_wrapper
def valid_remainder(cntxt: Context, n: nodeSelector, matchables: RDFGraph, S: ShExJ.Shape) -> bool:
    """
    Let **outs** be the arcsOut in remainder: `outs = remainder ∩ arcsOut(G, n)`.

    Let **matchables** be the triples in outs whose predicate appears in a TripleConstraint in `expression`. If
    `expression` is absent, matchables = Ø (the empty set).

    * There is no triple in **matchables** which matches a TripleConstraint in expression

    * There is no triple in **matchables** whose predicate does not appear in extra.

    * closed is false or unmatchables is empty

    :param cntxt: evaluation context
    :param n: focus node
    :param matchables: non-matched triples
    :param S: Shape being evaluated
    :return: True if remainder is valid
    """
    # TODO: Update this and satisfies to address the new algorithm
    # Let **outs** be the arcsOut in remainder: `outs = remainder ∩ arcsOut(G, n)`.
    outs = arcsOut(cntxt.graph, n).intersection(matchables)

    # predicates that in a TripleConstraint in `expression`
    predicates = predicates_in_expression(S, cntxt)

    # Let **matchables** be the triples in outs whose predicate appears in predicates. If
    # `expression` is absent, matchables = Ø (the empty set).
    matchables = RDFGraph(t for t in outs if str(t.p) in predicates)

    # There is no triple in **matchables** which matches a TripleConstraint in expression
    if matchables and S.expression is not None:
        tes = triple_constraints_in_expression(S.expression, cntxt)
        for m in matchables:
            if any(matchesTripleConstraint(cntxt, RDFGraph([m]), te) for te in tes):
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
    c = cntxt.debug_context
    if c.trace_matches:
        c.mplus()
        print(c.i(2, f"---> matches {c.d()} : {type(expr)}"))
        print(c.i(3, "triples", sorted('<' + str(t[1]) + '> : <' + str(t[2]) + '>' for t in T)))
        print()
    rval = matchesCardinality(cntxt, T, expr) and (expr.semActs is None or semActsSatisfied(expr.semActs, cntxt))
    if c.trace_matches:
        c.mminus()
        print(c.i(2, f"<--- matches {c.d()} {rval}"))
    return rval


@matches_wrapper
def matchesCardinality(cntxt: Context, T: RDFGraph, expr: Union[ShExJ.tripleExpr, ShExJ.tripleExprLabel]) -> bool:
    """ Evaluate cardinality expression
    expr has a cardinality of min and/or max not equal to 1, where a max of -1 is treated as unbounded, and
    T can be partitioned into k subsets T1, T2,…Tk such that min ≤ k ≤ max and for each Tn,
    matches(Tn, expr, m) by the remaining rules in this list.
    """
    # TODO: Cardinality defaults into spec
    # Set the cardinality defaults
    min_ = expr.min.val if expr.min.val is not None else 1
    max_ = expr.max.val if expr.max.val is not None else 1

    if len(T) < min_:
        return False
    partition_counter = 0

    if matchesExpr(cntxt, T, expr):
        return True

    # TODO: Check this out -- skipping partitions test may be less than ideal in this situation
    if min_ == 0:
        return True
    for partition in _partitions(T, min_, max_):
        partition_counter += 1
        if all(matchesExpr(cntxt, entry, expr) for entry in partition):
            return True
    return False


def _partitions(T: RDFGraph, min_: Optional[int], max_: Optional[int]) -> List[List[RDFGraph]]:
    if max_ == 1:
        yield [T]
        if min_ == 0:
            yield []
    else:
        for k in range(min_, (max(len(T), min_) if max_ == -1 else max_)+1):
            for partition in partition_t(T, k):
                yield partition


@matches_wrapper
def matchesExpr(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExpr) -> bool:
    """ Evaluate the expression

    """
    c = cntxt.debug_context
    if c.trace_matches:
        print(c.i(3, f"---> matchesExpr {c.d()}"))
    if isinstance(expr, ShExJ.OneOf):
        rval = matchesOneOf(cntxt, T, expr)
    elif isinstance(expr, ShExJ.EachOf):
        rval = matchesEachOf(cntxt, T, expr)
    elif isinstance(expr, ShExJ.TripleConstraint):
        rval = matchesTripleConstraint(cntxt, T, expr)
    elif isinstance(expr, ShExJ.tripleExprLabel):
        rval = matchesTripleExprRef(cntxt, T, expr)
    else:
        raise Exception("Unknown expression")
    if c.trace_matches:
        print(c.i(3, f"<---- matchesExpr {c.d()} {rval}"))
    return rval


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
    c = cntxt.debug_context
    if c.trace_matches:
        print(c.i(4, f"---> matchesEachOf {c.d()}",
              [f"{type(e)} : {e.predicate if isinstance(e, ShExJ.TripleConstraint) else ''}" for e in expr.expressions]))
        print()

    # Ad-hoc optimization -- we need to switch over to the regular expression solution that we did in the previous
    # implementation
    # The most common form of an eachOf is a list of triple expressions.  Before we go any further, we build an initial
    # candidate cluster
    partition_map: Dict[IRIREF, RDFGraph] = {}
    mixed_expression = False
    if c.trace_matches:
        print(f"({c.d()} depth: {c.eachof_depth})")
        print(expr._as_json_dumps())
    for e in expr.expressions:
        if isinstance(e, ShExJ.TripleConstraint):
            partition_map[e.predicate] = RDFGraph(t for t in T if str(t[1]) == str(e.predicate))
        else:
            mixed_expression = True
    if not mixed_expression:
        rslt = []
        for e in expr.expressions:
            c.eachof_depth += 1
            if c.trace_matches:
                print(c.i(c.eachof_depth, f"Processing ({c.eachof_depth})", e._as_json_dumps().split('\n')))
            rslt.append((e, matches(cntxt, partition_map[e.predicate], e)))
            rval = rslt[-1][1]
            if c.trace_matches:
                print(c.i(c.eachof_depth, f"   ({c.eachof_depth}){rslt[-1][1]}"))
                if not rval:
                    print(partition_map[e.predicate])
            c.eachof_depth -= 1
            if c.trace_matches:
                print()

        success = all(r[0] for r in rslt)
    else:
        success = False
    # success = not mixed_expression and all(matches(cntxt, partition_map[e.predicate], e) for e in expr.expressions)

    if not success and mixed_expression:
        for partition in _partitions(T, len(expr.expressions), len(expr.expressions)):
            if all(matches(cntxt, t, e) for t, e in zip(partition, expr.expressions)):
                success = True
                break
    if c.trace_matches:
        print(c.i(4, f"<---- matchesEachOf {c.d()} {success}"))
    return success


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

    c = cntxt.debug_context
    if c.trace_matches:
        if len(T) != 1:
            print(c.i(4, f"<---> matchesTripleConstraint {c.d()} False (len={len(T)})"))
        else:
            print(c.i(4, f"---> matchesTripleConstraint {c.d()}"))

    if len(T) == 1:
        for t in T:
            if uriref_matches_iriref(t.p, expr.predicate):
                value = t.s if expr.inverse.val else t.o
                if expr.valueExpr is None or satisfies(cntxt, value, expr.valueExpr):
                    if c.trace_matches:
                        print(c.i(4, f"<--- matchesTripleConstraint {c.d()} True"))
                    return True
                else:
                    if c.trace_matches:
                        print(c.i(4, f"---> matchesTripleConstraint {c.d()} "
                                     f"False - value {value} doesn't match"))
            else:
                if c.trace_matches:
                    print(c.i(4, f"---> matchesTripleConstraint {c.d()} "
                                 f"False - predicate {t.p} doesn't match {expr.predicate}"))
    return False


@matches_wrapper
def matchesTripleExprRef(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExprLabel) -> bool:
    """
    expr is an tripleExprRef and satisfies(value, tripleExprWithId(tripleExprRef), G, m).
    The tripleExprWithId function is defined in Triple Expression Reference Requirement below.
    """
    return matchesTripleConstraint(cntxt, T, cntxt.tripleExprFor(expr))
