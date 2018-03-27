""" Implementation of `5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_ """
from typing import Tuple, List

from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import FixedShapeMap, START


def isValid(cntxt: Context, m: FixedShapeMap) -> Tuple[bool, List[str]]:
    """`5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_

    The expression isValid(G, m) indicates that for every nodeSelector/shapeLabel pair (n, s) in m, s has a
        corresponding shape expression se and satisfies(n, se, G, m). satisfies is defined below for each form
        of shape expression

    :param cntxt: evaluation context - includes graph and schema
    :param m: list of NodeShape pairs to test
    :return: Success/failure indicator and, if fail, a list of failure reasons
    """
    return all(s is not None and satisfies(cntxt, n, s)
               for n, s in [(e.nodeSelector,
                             cntxt.shapeExprFor(e.shapeLabel if e.shapeLabel is START else
                                                START if e.shapeLabel is None else str(e.shapeLabel))) for e in m]), \
           cntxt.reasons
