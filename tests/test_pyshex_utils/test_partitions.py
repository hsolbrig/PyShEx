import unittest

from rdflib import Graph, RDF

from pyshex.utils.partitions import algorithm_u, partition_t
from tests.utils.setup_test import gen_rdf, rdf_header, EX


class PartitionsTestCase(unittest.TestCase):
    def test_algorithm_u(self):
        def organize(parts) -> str:
            return '; '.join('|'.join(''.join(str(e) for e in loe) for loe in part) for part in parts)

        x = list("abcde")
        permutations = [organize(algorithm_u(x, n)) for n in range(1, len(x) + 1)]
        self.assertEqual(
            ['abcde',
             'abcd|e; acd|be; ad|bce; abd|ce; ab|cde; a|bcde; ac|bde; abc|de; abce|d; '
             'ace|bd; ae|bcd; abe|cd; abde|c; ade|bc; acde|b',
             'abc|d|e; ab|cd|e; a|bcd|e; ac|bd|e; acd|b|e; ad|bc|e; abd|c|e; ab|c|de; '
             'a|bc|de; ac|b|de; a|b|cde; a|bd|ce; ad|b|ce; ad|be|c; a|bde|c; a|be|cd; '
             'ac|be|d; a|bce|d; ab|ce|d; abe|c|d; ae|bc|d; ace|b|d; ae|b|cd; ae|bd|c; '
             'ade|b|c',
             'ab|c|d|e; a|bc|d|e; ac|b|d|e; a|b|cd|e; a|bd|c|e; ad|b|c|e; a|b|c|de; '
             'a|b|ce|d; a|be|c|d; ae|b|c|d',
             'a|b|c|d|e'], permutations)
        self.assertEqual(
            [[[1], [2]]], list(algorithm_u([1, 2], 2)))

    def test_partition_t(self):
        triples = gen_rdf("""<Alice> ex:shoeSize "30"^^xsd:integer .
        <Alice> a ex:Teacher .
        <Alice> a ex:Person .
        <SomeHat> ex:owner <Alice> .
        <TheMoon> ex:madeOf <GreenCheese> .""")
        g = Graph()
        g.parse(data=triples, format="turtle")
        glist = list(g)
        for psize in range(1, len(glist)):
            l1 = algorithm_u(glist, 2)
            l2 = partition_t(glist, 2)
            for e1, e2 in zip(l1, l2):
                self.assertEqual(e1, e2)

    def test_caching(self):
        triples = gen_rdf("""<Alice> ex:shoeSize "30"^^xsd:integer .
                <Alice> a ex:Teacher .
                <Alice> a ex:Person .
                <SomeHat> ex:owner <Alice> .
                <TheMoon> ex:madeOf <GreenCheese> .""")
        g = Graph()
        g.parse(data=triples, format="turtle")
        glist = list(g)
        p1 = list(partition_t(glist, 2))
        p2 = list(partition_t(glist, 3))
        self.maxDiff = None
        self.assertEqual(list(partition_t(glist, 2)), list(p1))
        self.assertEqual(list(partition_t(glist, 3)), list(p2))

    def test_large_partition(self):
        g = Graph()
        g.parse(data=rdf_header, format="turtle")
        for i in range(25):
            g.add((EX['s' + str(i)], RDF.type, EX.thing))
        glist = sorted(list(g))
        part1 = partition_t(glist, 20, cached=False)
        # Skip to the 10t0h element in the partition
        [next(part1) for _ in range(100)]
        self.assertEqual([
             ['http://schema.example/s0', 'http://schema.example/s11'],
             ['http://schema.example/s1', 'http://schema.example/s10', 'http://schema.example/s12'],
             ['http://schema.example/s13', 'http://schema.example/s14', 'http://schema.example/s15'],
             ['http://schema.example/s16'],
             ['http://schema.example/s17'],
             ['http://schema.example/s18'],
             ['http://schema.example/s19'],
             ['http://schema.example/s2'],
             ['http://schema.example/s20'],
             ['http://schema.example/s21'],
             ['http://schema.example/s22'],
             ['http://schema.example/s23'],
             ['http://schema.example/s24'],
             ['http://schema.example/s3'],
             ['http://schema.example/s4'],
             ['http://schema.example/s5'],
             ['http://schema.example/s6'],
             ['http://schema.example/s7'],
             ['http://schema.example/s8'],
             ['http://schema.example/s9']], [[str(e[0]) for e in part] for part in next(part1)])
        part2 = partition_t(glist, 1)
        self.assertEqual(1, sum(1 for e in part2))
        part3 = partition_t(glist, 25)
        self.assertEqual(1, sum(1 for e in part3))


if __name__ == '__main__':
    unittest.main()
