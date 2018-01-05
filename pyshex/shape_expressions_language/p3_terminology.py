""" Implementation of `3. Terminology <http://shex.io/shex-semantics/#terminology>`_

    Shape expressions are defined using terms from RDF semantics [rdf11-mt]:

    * Node: one of IRI, blank node, Literal
    * Graph: a set of Triples of (subject, predicate, object)
"""
from typing import Set

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import Node, RDFTriple, TriplePredicate
from rdflib import Graph

# This specification makes use of the following namespaces:
from rdflib import RDF, RDFS, XSD
from rdflib import Namespace

SHEX = Namespace("http://www.w3.org/ns/shex#")


def arcsOut(G: Graph, n: Node) -> Set[RDFTriple]:
    """ arcsOut(G, n) is the set of triples in a graph G with subject n. """
    return set(G.triples((n, None, None)))


def predicatesOut(G: Graph, n: Node) -> Set[TriplePredicate]:
    """ predicatesOut(G, n) is the set of predicates in arcsOut(G, n). """
    return {p for p, _ in G.predicate_objects(n)}


def arcsIn(G: Graph, n: Node) -> Set[RDFTriple]:
    """ arcsIn(G, n) is the set of triples in a graph G with object n. """
    return set(G.triples((None, None, n)))


def predicatesIn(G: Graph, n: Node) -> Set[TriplePredicate]:
    """ predicatesIn(G, n) is the set of predicates in arcsIn(G, n). """
    return {p for _, p in G.subject_predicates(n)}


def neigh(G: Graph, n: Node) -> Set[RDFTriple]:
    """  neigh(G, n) is the neighbourhood of the node n in the graph G.

         neigh(G, n) = arcsOut(G, n) ∪ arcsIn(G, n)
    """
    return arcsOut(G, n) | arcsIn(G, n)


def predicates(G: Graph, n: Node) -> Set[TriplePredicate]:
    """ redicates(G, n) is the set of predicates in neigh(G, n).

        predicates(G, n) = predicatesOut(G, n) ∪ predicatesIn(G, n)
    """
    return predicatesOut(G, n) | predicatesIn(G, n)


