""" Implementation of `5.4 <http://shex.io/shex-semantics/#node-constraints>`_"""

import numbers
from typing import Union, Optional

from ShExJSG import ShExJ
from pyjsg.jsglib.jsg import isinstance_
from rdflib import URIRef, BNode, Literal, XSD, RDF

from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import Node
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.sparql11_query.p17_1_operand_data_types import is_sparql_operand_datatype, is_numeric
from pyshex.utils.datatype_utils import can_cast_to, total_digits, fraction_digits, pattern_match, map_object_literal
from pyshex.utils.value_set_utils import objectValueMatches, uriref_startswith_iriref, uriref_matches_iriref


def satisfies2(cntxt: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.1 Semantics <http://shex.io/shex-semantics/#node-constraint-semantics>`_

    For a node n and constraint nc, satisfies2(n, nc) if and only if for every nodeKind, datatype, xsFacet and
    values constraint value v present in nc nodeSatisfies(n, v). The following sections define nodeSatisfies for
    each of these types of constraints:
    """
    return nodeSatisfiesNodeKind(cntxt, n, nc) and nodeSatisfiesDataType(cntxt, n, nc) and \
        nodeSatisfiesStringFacet(cntxt, n, nc) and nodeSatisfiesNumericFacet(cntxt, n, nc) and \
        nodeSatisfiesValues(cntxt, n, nc)


def nodeSatisfiesNodeKind(_: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.2 Node Kind Constraints <http://shex.io/shex-semantics/#nodeKind>`_

    For a node n and constraint value v, nodeSatisfies(n, v) if:

        * v = "iri" and n is an IRI.
        * v = "bnode" and n is a blank node.
        * v = "literal" and n is a Literal.
        * v = "nonliteral" and n is an IRI or blank node.
    """
    return nc.nodeKind is None or \
        (nc.nodeKind == 'iri' and isinstance(n, URIRef)) or \
        (nc.nodeKind == 'bnode' and isinstance(n, BNode)) or \
        (nc.nodeKind == 'literal' and isinstance(n, Literal)) or \
        (nc.nodeKind == 'nonliteral' and isinstance(n, (URIRef, BNode)))


def nodeSatisfiesDataType(_: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.3 Datatype Constraints <http://shex.io/shex-semantics/#datatype>`_

    For a node n and constraint value v, nodeSatisfies(n, v) if n is an Literal with the datatype v and, if v is in
    the set of SPARQL operand data types[sparql11-query], an XML schema string with a value of the lexical form of
    n can be cast to the target type v per XPath Functions 3.1 section 19 Casting[xpath-functions]. Only datatypes
    supported by SPARQL MUST be tested but ShEx extensions MAY add support for other datatypes.
    """
    # TODO: reconcile this with rdflib and the spec
    # TODO: for all of these situations, create a special error when nodeSelector is None
    return nc.datatype is None or \
        (str(_datatype(n)) == nc.datatype and
         (not is_sparql_operand_datatype(nc.datatype) or (n.datatype is not None and can_cast_to(n, nc.datatype))))


def _datatype(n: nodeSelector) -> Optional[str]:
    return None if not isinstance(n, Literal) \
        else str(RDF.langString) if (n.datatype is None or n.datatype == XSD.string) and n.language else \
        str(n.datatype)


def nodeSatisfiesStringFacet(_: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.5 XML Schema String Facet Constraints <ttp://shex.io/shex-semantics/#xs-string>`_

     String facet constraints apply to the lexical form of the RDF Literals and IRIs and blank node
     identifiers (see note below regarding access to blank node identifiers).
    """

    # Let lex =
    #
    #  * if the value n is an RDF Literal, the lexical form of the literal (see[rdf11-concepts] section 3.3 Literals).
    #  * if the value n is an IRI, the IRI string (see[rdf11-concepts] section 3.2 IRIs).
    #  * if the value n is a blank node, the blank node identifier (see[rdf11-concepts] section 3.4 Blank Nodes).
    if nc.length.val is not None or nc.minlength.val is not None or nc.maxlength.val is not None \
            or nc.pattern.val is not None:
        lex = str(n)
        #  Let len = the number of unicode codepoints in lex
        # For a node n and constraint value v, nodeSatisfies(n, v):
        #
        #  * for "length" constraints, v = len,
        #  * for "minlength" constraints, v >= len,
        #  * for "maxlength" constraints, v <= len,
        #  * for "pattern" constraints, v is unescaped into a valid XPath 3.1 regular expression[xpath-functions-31]
        #    re and invoking fn:matches(lex, re) returns fn:true. If the flags parameter is present, it is passed
        #    as a third argument to fn:matches. The pattern may have XPath 3.1 regular expression escape sequences
        #    per the modified production [10] in section 5.6.1.1 as well as numeric escape sequences of the
        #    form 'u' HEX HEX HEX HEX or 'U' HEX HEX HEX HEX HEX HEX HEX HEX. Unescaping replaces numeric escape
        #    sequences with the corresponding unicode codepoint

        # TODO: Figure out whether we need to connect this to the lxml exslt functions
        # TODO: Map flags if not
        return (nc.length.val is None or len(lex) == nc.length.val) and \
               (nc.minlength.val is None or len(lex) >= nc.minlength.val) and \
               (nc.maxlength.val is None or len(lex) <= nc.maxlength.val) and \
               (nc.pattern.val is None or pattern_match(nc.pattern.val, nc.flags.val, lex))

    else:
        return True


def nodeSatisfiesNumericFacet(_: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.5 XML Schema Numeric Facet Constraints <http://shex.io/shex-semantics/#xs-numeric>`_

    Numeric facet constraints apply to the numeric value of RDF Literals with datatypes listed in SPARQL 1.1
    Operand Data Types[sparql11-query]. Numeric constraints on non-numeric values fail. totaldigits and
    fractiondigits constraints on values not derived from xsd:decimal fail.
    """
    if nc.mininclusive.val is not None or nc.minexclusive.val is not None or nc.maxinclusive.val is not None \
            or nc.maxexclusive.val is not None or nc.totaldigits.val is not None or nc.fractiondigits.val is not None:
        if is_numeric(n):
            v = n.value
            if isinstance(v, numbers.Number):
                return (nc.mininclusive.val is None or v >= nc.mininclusive.val) and \
                       (nc.minexclusive.val is None or v > nc.minexclusive.val) and \
                       (nc.maxinclusive.val is None or v <= nc.maxinclusive.val) and \
                       (nc.maxexclusive.val is None or v < nc.maxexclusive.val) and \
                       (nc.totaldigits.val is None or (total_digits(n) is not None and
                                                       total_digits(n) <= nc.totaldigits.val)) and \
                       (nc.fractiondigits.val is None or (fraction_digits(n) is not None and
                                                          fraction_digits(n) <= nc.fractiondigits.val))
            else:
                return False
        else:
            return False
    return True


def nodeSatisfiesValues(cntxt: Context, n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.5 Values Constraint <http://shex.io/shex-semantics/#values>`_

     For a node n and constraint value v, nodeSatisfies(n, v) if n matches some valueSetValue vsv in v.
    """
    return any(_nodeSatisfiesValue(cntxt, n, vsv) for vsv in nc.values) if nc.values is not None else True


def _nodeSatisfiesValue(cntxt: Context, n: nodeSelector, vsv: ShExJ.valueSetValue) -> bool:
    """
    A term matches a valueSetValue if:
        * vsv is an objectValue and n = vsv.
        * vsv is a Language with langTag lt and n is a language-tagged string with a language tag l and l = lt.
        * vsv is a IriStem, LiteralStem or LanguageStem with stem st and nodeIn(n, st).
        * vsv is a IriStemRange, LiteralStemRange or LanguageStemRange with stem st and exclusions excls and
          nodeIn(n, st) and there is no x in excls such that nodeIn(n, excl).
        * vsv is a Wildcard with exclusions excls and there is no x in excls such that nodeIn(n, excl).

    Note that ObjectLiteral is *not* typed in ShExJ.jsg, so we identify it by a lack of a 'type' variable

    .. note:: Mismatch with spec
        This won't work correctly if the stem value is passed in to nodeIn, as there will be no way to know whether
        we're matching an IRI or other type

    ... note:: Language issue
        The stem range spec shouldn't have the first element in the exclusions

    """
    vsv = map_object_literal(vsv)
    if isinstance_(vsv, ShExJ.objectValue):
        return objectValueMatches(n, vsv)

    if isinstance(vsv, ShExJ.Language):
        if vsv.languageTag is not None and isinstance(n, Literal) and n.language is not None:
            return n.language == vsv.languageTag
        else:
            return False

    if isinstance(vsv, ShExJ.IriStem):
        return nodeInIriStem(cntxt, n, vsv.stem)

    if isinstance(vsv, ShExJ.IriStemRange):
        exclusions = vsv.exclusions if vsv.exclusions is not None else []
        return nodeInIriStem(cntxt, n, vsv.stem) and not any(
            (uriref_matches_iriref(n, excl) if isinstance(excl, ShExJ.IRIREF) else
             uriref_startswith_iriref(n, excl.stem)) for excl in exclusions)

    if isinstance(vsv, ShExJ.LiteralStem):
        return nodeInLiteralStem(cntxt, n, vsv.stem)

    if isinstance(vsv, ShExJ.LiteralStemRange):
        exclusions = vsv.exclusions if vsv.exclusions is not None else []
        return nodeInLiteralStem(cntxt, n, vsv.stem) and not any(str(n) == excl for excl in exclusions)

    if isinstance(vsv, ShExJ.LanguageStem):
        return nodeInLanguageStem(cntxt, n, vsv.stem)

    if isinstance(vsv, ShExJ.LanguageStemRange):
        exclusions = vsv.exclusions if vsv.exclusions is not None else []
        return nodeInLanguageStem(cntxt, n, vsv.stem) and not any(str(n) == str(excl) for excl in exclusions)

    return False


def nodeInIriStem(_: Context, n: Node, s: ShExJ.IriStem) -> bool:
    """
       **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
       :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

       The expression `nodeInIriStem(n, s)` is satisfied iff:
        #) `s` is a :py:class:`ShExJ.WildCard` or
        #) `n` is an :py:class:`rdflib.URIRef` and fn:starts-with(`n`, `s`)
    """
    return isinstance(s, ShExJ.Wildcard) or \
        (isinstance(n, URIRef) and uriref_startswith_iriref(n, str(s)))


def nodeInLiteralStem(_: Context, n: Node, s: ShExJ.LiteralStem) -> bool:
    """ http://shex.io/shex-semantics/#values

        **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
        :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

        The expression `nodeInLiteralStem(n, s)` is satisfied iff:
         #) `s` is a :py:class:`ShExJ.WildCard` or
         #) `n` is an :py:class:`rdflib.Literal` and fn:starts-with(`n`, `s`)
     """
    return isinstance(s, ShExJ.Wildcard) or \
        (isinstance(n, Literal) and str(n.value).startswith(str(s)))


def nodeInLanguageStem(_: Context, n: Node, s: ShExJ.LanguageStem) -> bool:
    """ http://shex.io/shex-semantics/#values

        **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
        :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

        The expression `nodeInLanguageStem(n, s)` is satisfied iff:
         #) `s` is a :py:class:`ShExJ.WildCard` or
         #) `n` is a language-tagged string and fn:starts-with(`n.language`, `s`)
    """
    return isinstance(s, ShExJ.Wildcard) or \
        (isinstance(n, Literal) and n.language is not None and str(n.language).startswith(str(s)))


def nodeInBnodeStem(cntxt: Context, n: Node, s: Union[str, ShExJ.Wildcard]) -> bool:
    """ http://shex.io/shex-semantics/#values

        **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
        :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

        The expression `nodeInBnodeStem(n, s)` is satisfied iff:
         #) `s` is a :py:class:`ShExJ.WildCard` or
         #) `n` is a language-tagged string and fn:starts-with(`n.language`, `s`)

    """
    # TODO: resolve issue #79 to figure out how to do this
    return False
