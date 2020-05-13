import unittest

from rdflib import Graph, URIRef

from pyshex.utils import tortoise

tortoise.register()

class TortoiseTestCase(unittest.TestCase):
    def test_tortoise(self):
        g = Graph()
        self.assertEqual("""@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""", g.serialize(format="tortoise").decode().strip())
        g.bind('foo', 'http://example.org/foo#')
        g.add((URIRef('http://example.org/foo#a'),
               URIRef('http://example.org/foo#b'),
               URIRef('http://example.org/foo#c')))
        self.assertEqual("""@prefix foo: <http://example.org/foo#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

foo:a foo:b foo:c .""", g.serialize(format='tortoise').decode().strip())


if __name__ == '__main__':
    unittest.main()
