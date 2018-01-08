""" Implementation of `5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_ """

from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import FixedShapeMap
from pyshex.utils.debug_utils import basic_function_wrapper


@basic_function_wrapper
def isValid(cntxt: Context, m: FixedShapeMap) -> bool:
    """`5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_

    The expression isValid(G, m) indicates that for every nodeSelector/shapeLabel pair (n, s) in m, s has a
        corresponding shape expression se and satisfies(n, se, G, m). satisfies is defined below for each form
        of shape expression

    :param cntxt: evaluation context - includes graph and schema
    :param m: list of NodeShape pairs to test
    :return:
    """
    return all(s in cntxt.schema.shapes and satisfies(cntxt, n, cntxt.shapeExprFor(s))
               for n, s in [(e.nodeSelector, e.shapeLabel) for e in m])
