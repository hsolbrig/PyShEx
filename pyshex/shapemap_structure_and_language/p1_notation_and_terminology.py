from typing import Union, Tuple
from rdflib import URIRef, BNode, Literal

#  This document assumes an understanding of the ShEx notation and terminology.
#
#     ShapeExpression: a Boolean expression of ShEx shapes.
#     focus node: a node, potentially in an RDF graph, to be inspected for conformance with a shape expression.
#
# ShExMap uses the following terms from RDF semantics [rdf11-mt]:
#
#     Node: one of IRI, blank node, Literal.
#     Graph: a set of Triples of (subject, predicate, object).


# We have no idea what is intended in the above definition -- for the moment we'll define it as a function
# ShapeExpression = Callable[[List[ShExJ.Shape], bool]]
Node = Union[URIRef, BNode, Literal]
FocusNode = Node
TripleSubject = Union[URIRef, BNode]
TriplePredicate = URIRef
TripleObject = Union[URIRef, Literal, BNode]


class RDFTriple:
    def __init__(self, t_or_subject: Union[Tuple[TripleSubject, TriplePredicate, TripleObject]],
                 predicate: TriplePredicate=None,
                 object: TripleObject=None) -> None:
        self.subject: TripleSubject = t_or_subject if object else t_or_subject[0]
        self.predicate: TriplePredicate = predicate if predicate else t_or_subject[1]
        self.object: TripleObject = object if object else t_or_subject[2]

    def __lt__(self, other: "RDFTriple") -> bool:
        if self.subject == other.subject:
            if self.predicate == other.predicate:
                return self.object < other.object
            else:
                return self.predicate < other.predicate
        else:
            return self.subject < other .subject
