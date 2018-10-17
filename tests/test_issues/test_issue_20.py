import unittest

from pyshex import ShExEvaluator, PrefixLibrary

shex = """
BASE <http://example.org/ex/>
PREFIX ex: <example.org/ex/>
PREFIX : <http://hl7.org/fhir/>

start = @<BloodPressureMeasurementShape>

<BloodPressureMeasurementShape>  {
    (
        (:hasMethod [<invasive>] ;
         :hasLocation IRI{0})?
    |
        (:hasMethod [<non-invasive>]  ;
        | :hasLocation IRI)*
    )
} 

"""

rdf = """
BASE <http://example.org/ex/>
PREFIX ex: <http://example.org/ex/>
PREFIX : <http://hl7.org/fhir/>

<BPM1>
  :hasMethod <invasive> ;
  :hasLocation <BPMLocation1> .
  
<BPM2>
  :hasMethod <non-invasive> ;
  :hasLocation <BPMLocation2> .
"""


class BPM2TestCase(unittest.TestCase):
    @unittest.skipIf(True, "Test not complete")
    def test_fail(self):
        pl = PrefixLibrary(rdf)
        results = ShExEvaluator().evaluate(rdf, shex, focus=[pl.EX.BPM1, pl.EX.BPM2], debug=False)
        for r in results:
            if r.result:
                print("PASS")
            else:
                print(f"FAIL: {r.reason}")
        self.assertEqual([False, True], [r.result for r in results])
        self.assertEqual("A good fail reason", results[0].reason)


if __name__ == '__main__':
    unittest.main()
