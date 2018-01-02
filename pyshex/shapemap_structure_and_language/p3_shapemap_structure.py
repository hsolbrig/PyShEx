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
from typing import Union, NamedTuple, Any, Optional, Set

import jsonasobj
from jsonasobj import JsonObj
from rdflib import URIRef, Literal
from pyshex.utils.stringtoken import StringToken
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import Node

from ShExJSG import ShExJ


# From: https://www.w3.org/TR/sparql11-query/#sparqlBasicTerms
#
# Definition: RDF Term
#
# Let I be the set of all IRIs.
# Let RDF-L be the set of all RDF Literals
# Let RDF-B be the set of all blank nodes in RDF graphs
#
# The set of RDF Terms, RDF-T, is I ∪ RDF-L ∪ RDF-B.

RDF_Term = Node


# Definition: Query Variable
#
# A query variable is a member of the set V where V is infinite and disjoint from RDF-T.
class QueryVariable:
    def __init__(self, v: Any) -> None:
        assert not isinstance(v, RDF_Term)
        self.v = v


# https://www.w3.org/TR/sparql11-query/#sparqlTriplePatterns
# Definition: Triple Pattern
#
# A triple pattern is member of the set:
# (RDF-T ∪ V) x (I ∪ V) x (RDF-T ∪ V)
class SparqlTriplePattern(NamedTuple):
    subject: Union[RDF_Term, QueryVariable]
    predicate: Union[URIRef, QueryVariable]
    object: Union[RDF_Term, QueryVariable]


class FOCUS(StringToken):
    pass


class WILD_CARD(StringToken):
    def __str__(self):
        return "_"


# A focus selector identifies the slot (subject or object) to be validated. A wildcard indicates that the slot may hold
#  any value. A triple pattern has exactly one focus selector. A triple pattern maps to a SPARQL triple pattern with
#  the following restrictions:
#
#    * V (the set of variables) is either a fresh variable or a known token to identify the focus node.
#    * The focus node token appears in either the subject or the object position.
#    * The predicate position is filled by an IRI (I in the SPARQL definitions).
class SubjectFocusPattern(StringToken):
    subject: FOCUS
    predicate: URIRef
    object: Union[URIRef, Literal, WILD_CARD]


class ObjectFocusPattern(StringToken):
    subject: Union[URIRef, WILD_CARD]
    predicate: URIRef
    object: FOCUS


TriplePattern = Union[SubjectFocusPattern, ObjectFocusPattern]


class START(StringToken):
    pass


class conformant(StringToken):
    pass


class nonconformant(StringToken):
    pass


# http://shex.io/shape-map/#shapemap-structure
#
# ShapeMap: a set of shape associations. Each shape association has at least two members: a nodeSelector
# and a shapeLabel, and when used for the result of validation, may have any of status, reason, or appInfo:
#
#  * nodeSelector: an RDF node, or a triple pattern which is used to select RDF Nodes
#  * shapeLabel: ShEx shapeExprLabel or the string "START" for the start shape expression
#  * status: [default="conformant"] "nonconformant" or "conformant"
#  * reason: [optional] a string stating the reason for failure or success
#  * appInfo: [optional] an application-spscific JSON-LD structure

nodeSelector = Union[Node, TriplePattern]
shapeLabel = Union[ShExJ.shapeExprLabel, START]
status = Optional[Union[conformant, nonconformant]]
reason = Optional[str]
appinfo = Optional[jsonasobj.JsonObj]


# In this document, these members can be addressed with a '.' operator. For instance, a shape association A
# would have an A.nodeSelector member.
#
# If the status member is absent, the status is assumed to be "conformant". The reason and appInfo members may
# also be absent but have no default value.
class ShapeAssociation(JsonObj):
    def __init__(self, nodeSelector: nodeSelector, shapeLabel: shapeLabel, status: status=None, reason: reason=None,
                 appinfo: appinfo=None) -> None:
        self.nodeSelector = nodeSelector
        self.shapeLabel = shapeLabel
        self.status = status if status is not None else conformant,
        self.reason = reason
        self.appinfo = appinfo
        super().__init__()


# No two shape associations in a ShapeMap may have the same combination of nodeSelector and shapeLabel.
# NOTE: This means that, in fact, a ShapeMap is a mapping (dictionary) between a nodeSelector/shapeLabel tuple and
#       a status/reason/appinfo tuple
ShapeMapType = Set[ShapeAssociation]


class ShapeMap(set):
    def is_valid(self) -> bool:
        return len({(e.nodeSelector, e.shapeLabel) for e in self}) == len(self)


# A query shapeMap is a ShapeMap in which each shape association has only the members nodeSelector
# and shapeLabel.
class QueryShapeMap(ShapeMap):
    def is_valid(self) -> bool:
        return super().is_valid() and \
               all(e.status == conformant and e.reason is None and e.appinfo is None for e in self)


# A fixed ShapeMap is a query ShapeMap in which each nodeSelector is an RDF node. The ShEx validation
#  process takes as input a fixed ShapeMap.
class FixedShapeMap(QueryShapeMap):
    def is_valid(self) -> bool:
        return super().is_valid() and all(isinstance(e.nodeSelector, Node) for e in self)


# A result ShapeMap is a fixed ShapeMap with the addition of optional members status, reason and appInfo.
class ResultShapeMap(ShapeMap):
    def is_valid(self) -> bool:
        return super().is_valid() and all(isinstance(e.nodeSelector, Node) for e in self)
