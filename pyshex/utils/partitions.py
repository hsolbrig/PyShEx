"""
Partition utilities -
taken from `Stack Overflow <https://stackoverflow.com/questions/19368375/set-partitions-in-python>`_
"""
from typing import Set, List

import functools
from rdflib import Graph

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFTriple
from tests.utils.setup_test import gen_rdf

"""
taken from `Stack Overflow <https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions>`_

A python implementation of Knuth's algorithm.
"""

def algorithm_u(ns, m):
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a) if m > 1 else [[ns]]


@functools.lru_cache()
def integer_partition(size: int, nparts: int) -> List[List[List[int]]]:
    # Note: can't cache a generator (!)
    return list(algorithm_u(range(size), nparts))


def partition_t(T: List[RDFTriple], nparts: int, cached=True) -> List[List[List[RDFTriple]]]:
    """
    Partition T into all possible partitions of T of size nparts
    :param T: Set of RDF triples to be partitioned
    :param nparts: number of partitions (e.g. 2 means return all possible 2 set partitions
    :param cached: True means used the cached access
    :return: Iterator that returns partitions

    We don't actually partition the triples directly -- instead, we partition a set of integers that
    reference elements in the (ordered) set and return those
    """
    # TODO: the result of applying
    partitions = integer_partition(len(T), nparts) if cached else algorithm_u(range(len(T)), nparts)
    for partition in partitions:
        yield [[T[e] for e in element] for element in partition]
