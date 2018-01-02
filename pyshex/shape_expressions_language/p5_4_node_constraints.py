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
import numbers
from typing import Union

from ShExJSG import ShExJ
from ShExJSG.ShExJ import ObjectLiteral, IRIREF
from rdflib import URIRef, BNode, Literal, XSD, RDF

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import Node
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import nodeSelector
from pyshex.sparql11_query.p17_1_operand_data_types import is_sparql_operand_datatype, is_decimal
from pyshex.utils.datatype_utils import can_cast_to, total_digits, fraction_digits, pattern_match, map_object_literal
from pyshex.utils.value_set_utils import objectValueMatches, uriref_startswith_iriref


def satisfies2(n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """
    For a node n and constraint nc, satisfies2(n, nc) if and only if for every nodeKind, datatype, xsFacet and
    values constraint value v present in nc nodeSatisfies(n, v). The following sections define nodeSatisfies for
    each of these types of constraints: """
    return nodeSatisfiesNodeKind(n, nc) and nodeSatisfiesDataType(n, nc) and \
        nodeSatisfiesStringFacet(n, nc) and nodeSatisfiesNumericFacet(n, nc) and \
        nodeSatisfiesValues(n, nc)


def nodeSatisfiesNodeKind(n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ 5.4.2 Node Kind Constraints

    For a node n and constraint value v, nodeSatisfies(n, v) if:

        * v = "iri" and n is an IRI.
        * v = "bnode" and n is a blank node.
        * v = "literal" and n is a Literal.
        * v = "nonliteral" and n is an IRI or blank node.

    :param n:
    :param nc:
    :return:
    """
    return nc.nodeKind is None or \
        (nc.nodeKind == 'iri' and isinstance(n, URIRef)) or \
        (nc.nodeKind == 'bnode' and isinstance(n, BNode)) or \
        (nc.nodeKind == 'literal' and isinstance(n, Literal)) or \
        (nc.nodeKind == 'nonliteral' and isinstance(n, (URIRef, BNode)))


def nodeSatisfiesDataType(n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ `5.4.3 Datatype Constraints <http://shex.io/shex-semantics/#datatype>`_

    For a node n and constraint value v, nodeSatisfies(n, v) if n is an Literal with the datatype v and, if v is in
    the set of SPARQL operand data types[sparql11-query], an XML schema string with a value of the lexical form of
    n can be cast to the target type v per XPath Functions 3.1 section 19 Casting[xpath-functions]. Only datatypes
    supported by SPARQL MUST be tested but ShEx extensions MAY add support for other datatypes.
    :param n:
    :param nc:
    :return:
    """
    # TODO: reconcile this with rdflib and the spec
    # TODO: for all of these situations, create a special error when nodeSelector is None
    datatype = RDF.langString if (n.datatype is None or n.datatype == XSD.string) and n.language else n.datatype
    return nc.datatype is None or \
        (isinstance(n, Literal) and str(datatype) == nc.datatype and n.value is not None and
         (not is_sparql_operand_datatype(nc.datatype) or can_cast_to(n, nc.datatype)))


def nodeSatisfiesStringFacet(n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ 5.4.4 XML Schema String Facet Constraints

     String facet constraints apply to the lexical form of the RDF Literals and IRIs and blank node
     identifiers (see note below regarding access to blank node identifiers).
    :param n:
    :param nc:
    :return:
    """

    # Let lex =
    #
    #  * if the value n is an RDF Literal, the lexical form of the literal (see[rdf11-concepts] section 3.3 Literals).
    #  * if the value n is an IRI, the IRI string (see[rdf11-concepts] section 3.2 IRIs).
    #  * if the value n is a blank node, the blank node identifier (see[rdf11-concepts] section 3.4 Blank Nodes).
    if isinstance(n, (URIRef, BNode, Literal)):
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


def nodeSatisfiesNumericFacet(n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ 5.4.5 XML Schema Numeric Facet Constraints

    Numeric facet constraints apply to the numeric value of RDF Literals with datatypes listed in SPARQL 1.1
    Operand Data Types[sparql11-query]. Numeric constraints on non-numeric values fail. totaldigits and
    fractiondigits constraints on values not derived from xsd:decimal fail.
    """
    if is_decimal(n):
        v = n.value
        if isinstance(v, numbers.Number):
            return (nc.mininclusive.val is None or v >= nc.mininclusive.val) and \
                   (nc.minexclusive.val is None or v > nc.minexclusive.val) and \
                   (nc.maxinclusive.val is None or v <= nc.maxexclusive.val) and \
                   (nc.maxexclusive.val is None or v < nc.maxexclusive.val) and \
                   (nc.totaldigits.val is None or total_digits(n) == nc.totaldigits.val) and \
                   (nc.fractiondigits.val is None or fraction_digits(n) == nc.fractiondigits.val)


def nodeSatisfiesValues(n: nodeSelector, nc: ShExJ.NodeConstraint) -> bool:
    """ 5.4.6 Values Constraint

     For a node n and constraint value v, nodeSatisfies(n, v) if n matches some valueSetValue vsv in v.
    """
    return any(nodeSatisfiesValue(n, vsv) for vsv in nc.values) if nc.values is not None else True


def nodeSatisfiesValue(n: nodeSelector, vsv: ShExJ.valueSetValue) -> bool:
    """ http://shex.io/shex-semantics/#values

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
    if isinstance(vsv, (IRIREF, ObjectLiteral)):
        return objectValueMatches(n, vsv)

    if isinstance(vsv, ShExJ.Language):
        if vsv.languageTag is not None and isinstance(n, Literal) and n.language is not None:
            return n.language == vsv.languageTag
        else:
            return False

    if isinstance(vsv, ShExJ.IriStem):
        return nodeInIriStem(n, vsv.stem)

    if isinstance(vsv, ShExJ.IriStemRange):
        exclusions = vsv.exclusions if vsv.exclusions is not None else []
        return nodeInIriStem(n, vsv.stem) and not any(nodeInIriStem(n, excl.stem) for excl in exclusions)

    if isinstance(vsv, ShExJ.LiteralStem):
        return nodeInLiteralStem(n, vsv.stem)

    if isinstance(vsv, ShExJ.LiteralStemRange):
        exclusions = vsv.exclusions if vsv.exclusions is not None else []
        return nodeInLiteralStem(n, vsv.stem) and not any(nodeInLiteralStem(n, excl.stem) for excl in exclusions)

    if isinstance(vsv, ShExJ.LanguageStem):
        return nodeInLanguageStem(n, vsv.stem)

    if isinstance(vsv, ShExJ.LiteralStemRange):
        exclusions = vsv.exclusions if vsv.exclusions is not None else []
        return nodeInLanguageStem(n, vsv.stem) and not any(nodeInLanguageStem(n, excl.stem) for excl in exclusions)

    return False


def nodeInIriStem(n: Node, s: Union[ShExJ.IRIREF, ShExJ.Wildcard]) -> bool:
    """ http://shex.io/shex-semantics/#values

       **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
       :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

       The expression `nodeInIriStem(n, s)` is satisfied iff:
        #) `s` is a :py:class:`ShExJ.WildCard` or
        #) `n` is an :py:class:`rdflib.URIRef` and fn:starts-with(`n`, `s`)
    """
    return isinstance(s, ShExJ.Wildcard) or \
        (isinstance(n, URIRef) and uriref_startswith_iriref(n, s))


def nodeInLiteralStem(n: Node, s: Union[str, ShExJ.Wildcard]) -> bool:
    """ http://shex.io/shex-semantics/#values

        **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
        :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

        The expression `nodeInLiteralStem(n, s)` is satisfied iff:
         #) `s` is a :py:class:`ShExJ.WildCard` or
         #) `n` is an :py:class:`rdflib.Literal` and fn:starts-with(`n`, `s`)
     """
    return isinstance(s, ShExJ.Wildcard) or \
        (isinstance(n, Literal) and str(n.value).startswith(s))


def nodeInLanguageStem(n: Node, s: Union[ShExJ.LANGTAG, ShExJ.Wildcard]) -> bool:
    """ http://shex.io/shex-semantics/#values

        **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
        :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

        The expression `nodeInLanguageStem(n, s)` is satisfied iff:
         #) `s` is a :py:class:`ShExJ.WildCard` or
         #) `n` is a language-tagged string and fn:starts-with(`n.language`, `s`)
    """
    return isinstance(s, ShExJ.Wildcard) or \
        (isinstance(n, Literal) and n.language is not None and str(n.language).startswith(str(s)))


def nodeInBnodeStem(n: Node, s: Union[str, ShExJ.Wildcard]) -> bool:
    """ http://shex.io/shex-semantics/#values

        **nodeIn**: asserts that an RDF node n is equal to an RDF term s or is in a set defined by a
        :py:class:`ShExJ.IriStem`, :py:class:`LiteralStem` or :py:class:`LanguageStem`.

        The expression `nodeInBnodeStem(n, s)` is satisfied iff:
         #) `s` is a :py:class:`ShExJ.WildCard` or
         #) `n` is a language-tagged string and fn:starts-with(`n.language`, `s`)

    """
    # TODO: resolve issue #79 to figure out how to do this
    return False
