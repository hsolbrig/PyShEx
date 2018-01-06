from typing import Union

from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF
from rdflib import URIRef, Literal, XSD

from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.sparql11_query.p17_1_operand_data_types import is_decimal, is_integer


def objectValueMatches(n: nodeSelector, vsv: ShExJ.objectValue) -> bool:
    """ http://shex.io/shex-semantics/#values

    Implements "n = vsv" where vsv is an objectValue and n is a Node

    Note that IRIREF is a string pattern, so the matching type is str
    """
    return \
        (isinstance(vsv, IRIREF) and isinstance(n, URIRef) and uriref_matches_iriref(n, vsv)) or \
        (isinstance(vsv, ShExJ.ObjectLiteral) and isinstance(n, Literal) and literal_matches_objectliteral(n, vsv))


def uriref_matches_iriref(v1: URIRef, v2: Union[str, ShExJ.IRIREF]) -> bool:
    """ Compare :py:class:`rdflib.URIRef` value with :py:class:`ShExJ.IRIREF` value """
    return str(v1) == str(v2)


def uriref_startswith_iriref(v1: URIRef, v2: Union[str, ShExJ.IRIREF]) -> bool:
    """ Determine whether a :py:class:`rdflib.URIRef` value starts with the text of a :py:class:`ShExJ.IRIREF` value """
    return str(v1).startswith(str(v2))


def literal_matches_objectliteral(v1: Literal, v2: ShExJ.ObjectLiteral) -> bool:
    """ Compare :py:class:`rdflib.Literal` with :py:class:`ShExJ.objectLiteral` """
    v2_lit = Literal(v2.value, datatype=v2.type, lang=v2.language)
    return v1 == v2_lit
