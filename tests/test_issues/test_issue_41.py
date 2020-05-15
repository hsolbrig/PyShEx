import unittest
from pprint import pprint

from rdflib import Graph, Namespace

from pyshex import ShExEvaluator

rdf = """
@prefix : <http://example.org/model/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
<http://example.org/context/42> a :Person ;
    foaf:age 43 ;
    foaf:firstName "Bob",
        "Joe" ;
    foaf:lastName "smith" .
"""

shex = """
<http://example.org/sample/example1/String> <http://www.w3.org/2001/XMLSchema#string>
<http://example.org/sample/example1/Int> <http://www.w3.org/2001/XMLSchema#integer>
<http://example.org/sample/example1/Boolean> <http://www.w3.org/2001/XMLSchema#boolean>
<http://example.org/sample/example1/Person> CLOSED {
    (  <http://xmlns.com/foaf/0.1/firstName> @<http://example.org/sample/example1/String> * ;
       <http://xmlns.com/foaf/0.1/lastName> @<http://example.org/sample/example1/String> ;
       <http://xmlns.com/foaf/0.1/age> @<http://example.org/sample/example1/Int> ? ;
       <http://example.org/model/living> @<http://example.org/sample/example1/Boolean> ? ;
       <http://xmlns.com/foaf/0.1/knows> @<http://example.org/sample/example1/Person> *
    )
}
"""

EXC = Namespace("http://example.org/context/")
EXE = Namespace("http://example.org/sample/example1/")


class Issue41TestCase(unittest.TestCase):
    def test_closed(self):
        """ Test closed definition """

        e = ShExEvaluator(rdf=rdf, schema=shex, focus=EXC['42'], start=EXE.Person)
        
        pprint(e.evaluate())
        self.assertFalse(e.evaluate()[0].result)

        from pyshex.evaluate import evaluate
        g = Graph()
        g.parse(data=rdf, format="turtle")
        pprint(evaluate(g, shex, focus=EXC['42'], start=EXE.Person))



if __name__ == '__main__':
    unittest.main()
