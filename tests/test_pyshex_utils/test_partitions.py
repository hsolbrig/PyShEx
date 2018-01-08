import unittest

from rdflib import Graph, RDF, Literal, XSD, URIRef

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph
from pyshex.utils.partitions import algorithm_u, partition_t, partition_2
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
        glist = sorted(list(g))
        self.maxDiff = None
        for psize in range(1, len(glist)):
            l1 = [[RDFGraph(e) for e in part] for part in algorithm_u(glist, 2)]
            l2 = list(partition_t(RDFGraph(glist), 2))
            for e1, e2 in zip(l1, l2):
                self.assertEqual(e1, e2)

    def test_partition_2(self):
        # Len(partition) == 2**len(graph)
        g = Graph()
        x = list(partition_2(RDFGraph(g)))      # partition_2 is a generator - you can only do it once
        self.assertEqual(1, len(x))
        self.assertEqual([(RDFGraph(), RDFGraph())], x)

        triples = gen_rdf("""<Alice> ex:shoeSize "30"^^xsd:integer .""")
        g = Graph()
        g.parse(data=triples, format="turtle")
        self.assertEqual(2, len(list(partition_2(RDFGraph(g)))))

        # Two elements give 4 partitions ((e1, e2), ()), ((e1), (e2)), ((e2), (e1)), ((), (e1, e2))
        triples = gen_rdf("""<Alice> ex:shoeSize "30"^^xsd:integer .
                <Alice> a ex:Teacher .""")
        g = Graph()
        g.parse(data=triples, format="turtle")
        x = list(partition_2(RDFGraph(g)))
        self.assertEqual(4, len(x))

        triples = gen_rdf("""<Alice> ex:shoeSize "30"^^xsd:integer .
                        <Alice> a ex:Teacher .
                        <Alice> a ex:Person .""")
        g = Graph()
        g.parse(data=triples, format="turtle")
        self.assertEqual(8, len(list(partition_2(RDFGraph(g)))))

        triples = gen_rdf("""<Alice> ex:shoeSize "30"^^xsd:integer .
                        <Alice> a ex:Teacher .
                        <Alice> a ex:Person .
                        <Alice> a ex:Fool .""")
        g = Graph()
        g.parse(data=triples, format="turtle")
        self.assertEqual(16, len(list(partition_2(RDFGraph(g)))))

    def test_large_partition(self):
        # The reason for this test is to be certain that we get generators all the way through.  This test
        # will take forever if, somewhere in the process, we actually realize the whole partition
        g = Graph()
        g.parse(data=rdf_header, format="turtle")
        for i in range(25):
            g.add((EX['s' + str(i)], RDF.type, EX.thing))
        rdfg = RDFGraph(g)
        part1 = partition_t(rdfg, 20)
        # Skip to the 100th element in the partition
        [next(part1) for _ in range(100)]
        self.assertEqual([
             {'http://schema.example/s0', 'http://schema.example/s11'},
             {'http://schema.example/s1', 'http://schema.example/s10', 'http://schema.example/s12'},
             {'http://schema.example/s15', 'http://schema.example/s14', 'http://schema.example/s13'},
             {'http://schema.example/s16'},
             {'http://schema.example/s17'},
             {'http://schema.example/s18'},
             {'http://schema.example/s19'},
             {'http://schema.example/s2'},
             {'http://schema.example/s20'},
             {'http://schema.example/s21'},
             {'http://schema.example/s22'},
             {'http://schema.example/s23'},
             {'http://schema.example/s24'},
             {'http://schema.example/s3'},
             {'http://schema.example/s4'},
             {'http://schema.example/s5'},
             {'http://schema.example/s6'},
             {'http://schema.example/s7'},
             {'http://schema.example/s8'},
             {'http://schema.example/s9'}], [{str(list(e)[0]) for e in part} for part in next(part1)])
        part2 = partition_t(rdfg, 1)
        self.assertEqual(1, sum(1 for e in part2))
        part3 = partition_t(rdfg, 25)
        self.assertEqual(1, sum(1 for e in part3))


if __name__ == '__main__':
    unittest.main()
