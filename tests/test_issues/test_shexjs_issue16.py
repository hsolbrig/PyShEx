import unittest

from rdflib import Graph, Namespace, XSD, Literal

from pyshex import ShExEvaluator


FHIR = Namespace("http://hl7.org/fhir")
EX = Namespace("http://example.org/")

shex = f"""PREFIX : <{FHIR}>
PREFIX xsd: <{XSD}>

start = @:ObservationShape

:ObservationShape {{               # An Observation has:
  (:status xsd:integer* | :status xsd:string* )*
}}
"""


class ShexjsIssue16TestCase(unittest.TestCase):
    # Test of https://github.com/shexSpec/shex.js/issues/16

    def test_infinite_loop(self):
        g = Graph()
        g.add((EX.Obs1, FHIR.status, Literal("final")))
        e = ShExEvaluator(rdf=g, schema=shex, focus=EX.Obs1, start=FHIR.ObservationShape, debug=False)
        self.assertTrue(e.evaluate()[0].result)


if __name__ == '__main__':
    unittest.main()
