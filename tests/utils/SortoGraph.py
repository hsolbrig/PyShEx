from typing import NamedTuple, Union, Tuple, Optional, Generator

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.term import Node

QueryTriple = Tuple[Optional[URIRef], Optional[URIRef], Optional[Union[Literal, URIRef]]]

SUBJ = Union[URIRef, BNode]
PRED = URIRef
OBJ = Node


class RDFTriple(NamedTuple):
    s: SUBJ = None
    p: PRED = None
    o: OBJ = None


class SortOGraph(Graph):
    """ rdflib Graph wrapper that sorts the outputs
    """

    def triples(self,
                pattern: Optional[Union[QueryTriple, SUBJ]]) -> Generator[RDFTriple, None, None]:
        for t in sorted(super().triples(pattern)):
            yield t
