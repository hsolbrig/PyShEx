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


