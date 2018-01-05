from ShExJSG import ShExJ
from ShExJSG.ShExJ import IRIREF
from rdflib import URIRef, Literal

from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector


def objectValueMatches(n: nodeSelector, vsv: ShExJ.objectValue) -> bool:
    """ http://shex.io/shex-semantics/#values

    Implements "n = vsv" where vsv is an objectValue and n is a Node

    Note that IRIREF is a string pattern, so the matching type is str
    """
    return \
        (isinstance(vsv, IRIREF) and isinstance(n, URIRef) and uriref_matches_iriref(n, vsv)) or \
        (isinstance(vsv, ShExJ.ObjectLiteral) and isinstance(n, Literal) and literal_matches_objectliteral(n, vsv))


def uriref_matches_iriref(v1: URIRef, v2: ShExJ.IRIREF) -> bool:
    """ Compare :py:class:`rdflib.URIRef` value with :py:class:`ShExJ.IRIREF` value """
    return str(v1) == str(v2)


def uriref_startswith_iriref(v1: URIRef, v2: ShExJ.IRIREF) -> bool:
    """ Determine whether a :py:class:`rdflib.URIRef` value starts with the text of a :py:class:`ShExJ.IRIREF` value """
    return str(v1).startswith(str(v2))


def literal_matches_objectliteral(v1: Literal, v2: ShExJ.ObjectLiteral) -> bool:
    """ Compare :py:class:`rdflib.Literal` with :py:class:`ShExJ.objectLiteral` """
    return str(v1.value) == str(v2.value) and \
           (v2.language is None or v1.language == v2.language) and \
           (v2.type is None or uriref_matches_iriref(v1.datatype, v2.type))