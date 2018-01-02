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
from typing import Union, Callable, List, Tuple, NamedTuple
from ShExJSG import ShExJ

#  This document assumes an understanding of the ShEx notation and terminology.
#
#     ShapeExpression: a Boolean expression of ShEx shapes.
#     focus node: a node, potentially in an RDF graph, to be inspected for conformance with a shape expression.
#
# ShExMap uses the following terms from RDF semantics [rdf11-mt]:
#
#     Node: one of IRI, blank node, Literal.
#     Graph: a set of Triples of (subject, predicate, object).

from rdflib import URIRef, BNode, Literal, Graph

# We have no idea what is intended in the above definition -- for the moment we'll define it as a function
# ShapeExpression = Callable[[List[ShExJ.Shape], bool]]
Node = Union[URIRef, BNode, Literal]
FocusNode = Node
TripleSubject = Union[URIRef, BNode]
TriplePredicate = URIRef
TripleObject = Union[URIRef, Literal, BNode]


class RDFTriple(NamedTuple):
    subject: TripleSubject
    predicate: TriplePredicate
    object: TripleObject
