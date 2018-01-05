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
