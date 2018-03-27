""" Implementation of `5.5 Shapes and Triple Expressions <http://shex.io/shex-semantics/#shapes-and-TEs>`_"""

from typing import List, Optional, Union, Dict

from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF
from pyjsg.jsglib.jsg import isinstance_
from sparql_slurper import SlurpyGraph

from pyshex.shape_expressions_language.p3_terminology import arcsOut
from pyshex.shape_expressions_language.p5_7_semantic_actions import semActsSatisfied
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph, RDFTriple
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.utils.partitions import partition_t, partition_2
from pyshex.utils.schema_utils import predicates_in_expression, triple_constraints_in_expression, \
    directed_predicates_in_expression
from pyshex.utils.slurp_utils import slurper
from pyshex.utils.value_set_utils import uriref_matches_iriref, iriref_to_uriref


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

    # Recursion detection.  If start_evaluating returns a boolean value, this is the assumed result of the shape
    # evaluation.  If it returns None, then an initial evaluation is needed
    rslt = cntxt.start_evaluating(n, S)

    predicates = directed_predicates_in_expression(S, cntxt)
    matchables = RDFGraph()
    c = cntxt.debug_context

    # Note: The code below does an "over-slurp" for the sake of expediency.  If you are interested in
    #       getting EXACTLY the needed triples, set cntxt.over_slurp to false
    if isinstance(cntxt.graph, SlurpyGraph) and cntxt.over_slurp:
        with slurper(cntxt, n, S) as g:
            _ = g.triples((n, None, None))

    for predicate, direction in predicates.items():
        with slurper(cntxt, n, S) as g:
            matchables.add_triples(g.triples((n if direction.is_fwd else None,
                                              iriref_to_uriref(predicate),
                                              n if direction.is_rev else None)))

    if c.trace_satisfies:
        print(c.i(c.satisfies_depth, f"---> Satisfies shape {c.d()}"))
        print(c.i(c.satisfies_depth+1, f"subject: {n}"))
        print(c.i(c.satisfies_depth+1, "predicates:", sorted(str(p) for p in predicates.keys())))
        print(c.i(c.satisfies_depth+1, "matchables:", sorted(str(m) for m in matchables)))
        print()

    if S.closed.val:
        # TODO: Is this working correctly on reverse items?
        non_matchables = RDFGraph([t for t in arcsOut(cntxt.graph, n) if t not in matchables])
        if len(non_matchables):
            cntxt.reasons.append("Unmatched triples in CLOSED shape:")
            cntxt.reasons += [f"\t{t}" for t in non_matchables]
            if c.trace_satisfies:
                print(c.i(c.satisfies_depth,
                          f"<--- Satisfies shape {c.d()} FAIL - "
                          f"{len(non_matchables)} non-matching triples on a closed shape"))
                print(c.i(c.satisfies_depth+1, "", non_matchables))
                print()
            rslt = False

    if rslt is None:
        # Evaluate the actual expression.  Start assuming everything matches...
        if S.expression:
            if matches(cntxt, matchables, S.expression):
                rslt = True
            else:
                extras = {iriref_to_uriref(e) for e in S.extra} if S.extra is not None else {}
                if len(extras):
                    permutable_matchables = RDFGraph([t for t in matchables if t.p in extras])
                    non_permutable_matchables = RDFGraph([t for t in matchables if t not in permutable_matchables])
                    if c.trace_satisfies:
                        print(c.i(c.satisfies_depth+1,
                                  f"\nComplete match failed -- evaluating extras", extras))
                    for matched, remainder in partition_2(permutable_matchables):
                        permutation = non_permutable_matchables.union(matched)
                        if matches(cntxt, permutation, S.expression):
                            rslt = True
                            break
                rslt = rslt or False
        else:
            rslt = True         # Empty shape

        # If an assumption was made and the result doesn't match the assumption, switch directions and try again
        done, consistent = cntxt.done_evaluating(n, S, rslt)
        if not done:
            rslt = satisfiesShape(cntxt, n, S)
        rslt = rslt and consistent
    if c.trace_satisfies:
        print(c.i(c.satisfies_depth, f"<--- Satisfies shape {c.d()} {rslt}"))
    return rslt


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
            if any(matchesTripleConstraint(cntxt, m, te) for te in tes):
                return False

    # There is no triple in **matchables** whose predicate does not appear in extra.
    extras = {iriref_to_uriref(e) for e in S.extra} if S.extra is not None else {}
    if any(t.p not in extras for t in matchables):
        return False

    # closed is false or unmatchables is empty.
    return not S.closed.val or not bool(outs - matchables)


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
    return matchesCardinality(cntxt, T, expr) and (expr.semActs is None or semActsSatisfied(expr.semActs, cntxt))


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
    if matchesExpr(cntxt, T, expr):
        return True
    for partition in _partitions(T, min_, max_):
        # print(f"Partition({min_}, {max_}): {','.join(str(len(e)) for e in partition)}")
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


def matchesExpr(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExpr) -> bool:
    """ Evaluate the expression

    """
    if isinstance(expr, ShExJ.OneOf):
        return matchesOneOf(cntxt, T, expr)
    elif isinstance(expr, ShExJ.EachOf):
        return matchesEachOf(cntxt, T, expr)
    elif isinstance(expr, ShExJ.TripleConstraint):
        return all(matchesTripleConstraint(cntxt, t, expr) for t in T)
    elif isinstance(expr, ShExJ.tripleExprLabel):
        return matchesTripleExprRef(cntxt, T, expr)
    else:
        raise Exception("Unknown expression")


def matchesOneOf(cntxt: Context, T: RDFGraph, expr: ShExJ.OneOf) -> bool:
    """
    expr is a OneOf and there is some shape expression se2 in shapeExprs such that a matches(T, se2, m).
    :param T:
    :param expr:
    :param cntxt:
    :return:
    """
    return any(matches(cntxt, T, e) for e in expr.expressions)


def matchesEachOf(cntxt: Context, T: RDFGraph, expr: ShExJ.EachOf) -> bool:
    """ expr is an EachOf and there is some partition of T into T1, T2,… such that for every expression
     expr1, expr2,… in shapeExprs, matches(Tn, exprn, m).
     """

    # Divide the graph up into potential candidates
    partition_map: Dict[IRIREF, RDFGraph] = {}
    expression_map: Dict[IRIREF, List[ShExJ.TripleConstraint]] = {}

    complex_expression = False          # True means one or more expression isn't a triple constraint

    for e in expr.expressions:
        if isinstance(e, ShExJ.TripleConstraint):
            if e.predicate in expression_map:
                expression_map[e.predicate].append(e)
            else:
                partition_map[e.predicate] = RDFGraph(t for t in T if str(t[1]) == str(e.predicate))
                expression_map[e.predicate] = [e]
        else:
            complex_expression = True
            break

    if not complex_expression:
        # We only have triple expressions
        for predicate, expr_list in expression_map.items():
            if len(expr_list) == 1 and not matches(cntxt, partition_map[predicate], expr_list[0]):
                success = False
            else:
                successful_combination = False
                for partition in _partitions(partition_map[predicate], len(expr_list), len(expr_list)):
                    if all(matches(cntxt, t, e) for t, e in zip(partition, expr_list)):
                        successful_combination = True
                        break
                success = successful_combination
            if not success:
                return False
        return True
    else:
        # One or more expressions is another shape or the like, we have to do this the hard way
        successful_combination = False
        for partition in _partitions(T, len(expr.expressions), len(expr.expressions)):
            if all(matches(cntxt, t, e) for t, e in zip(partition, expr.expressions)):
                successful_combination = True
                break
        return successful_combination


def matchesTripleConstraint(cntxt: Context, t: RDFTriple, expr: ShExJ.TripleConstraint) -> bool:
    """
    expr is a TripleConstraint and:

    * t is a triple
    * t's predicate equals expr's predicate.
      Let value be t's subject if inverse is true, else t's object.
    * if inverse is true, t is in arcsIn, else t is in arcsOut.

    """
    from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies

    if uriref_matches_iriref(t.p, expr.predicate):
        value = t.s if expr.inverse.val else t.o
        if expr.valueExpr is None or satisfies(cntxt, value, expr.valueExpr):
            return True
        else:
            return False
    else:
        return False


def matchesTripleExprRef(cntxt: Context, T: RDFGraph, expr: ShExJ.tripleExprLabel) -> bool:
    """
    expr is an tripleExprRef and satisfies(value, tripleExprWithId(tripleExprRef), G, m).
    The tripleExprWithId function is defined in Triple Expression Reference Requirement below.
    """
    expr = cntxt.tripleExprFor(expr)
    return all(matchesTripleConstraint(cntxt, t, expr) for t in T)
