import unittest
from contextlib import redirect_stdout
from io import StringIO
from typing import Callable

from rdflib import RDF, URIRef

from pyshex import ShExEvaluator
from pyshex.shex_evaluator import EvaluationResult, evaluate_cli
from tests.utils.SortoGraph import SortOGraph

rdf = '''
@prefix ex: <http://example.org/test/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:zrror1 rdf:type ex:S.
ex:pass1 rdf:type ex:S;
     ex:foo "a".
ex:pass2 rdf:type ex:S;
     ex:foo "b".
ex:zrror2 rdf:type ex:S.
ex:zrror3 rdf:type ex:S.
ex:zrror4 rdf:type ex:S.  
ex:pass3 rdf:type ex:S;
     ex:foo "c".
'''

shex = '''
PREFIX ex: <http://example.org/test/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
BASE <http://example.org/test/>

START=@<S>

<S> {a [ex:S]; ex:foo xsd:string}
'''

expected = [(URIRef('http://example.org/test/zrror1'),
             '  Testing ex:zrror1 against shape http://example.org/test/S\n'
             '       No matching triples found for predicate ex:foo'),
            (URIRef('http://example.org/test/zrror2'),
             '  Testing ex:zrror2 against shape http://example.org/test/S\n'
             '       No matching triples found for predicate ex:foo'),
            (URIRef('http://example.org/test/zrror3'),
             '  Testing ex:zrror3 against shape http://example.org/test/S\n'
             '       No matching triples found for predicate ex:foo'),
            (URIRef('http://example.org/test/zrror4'),
             '  Testing ex:zrror4 against shape http://example.org/test/S\n'
             '       No matching triples found for predicate ex:foo')]


class ErrorReportingUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.g = SortOGraph()
        cls.g.parse(data=rdf, format="turtle")

    def create_sink(self, failonerror: bool = False) -> Callable[[EvaluationResult], bool]:
        self.messages = []

        def sink(r: EvaluationResult) -> bool:
            if not r.result:
                self.messages.append((r.focus, r.reason))
                return not failonerror
            return True
        return sink

    def test_builtin_reports(self):
        """ Test built in output sink """

        # Test one - no output sink
        results = ShExEvaluator().evaluate(rdf, shex,  focus=list(self.g.subjects(RDF.type)))
        output = [(r.focus, r.reason) for r in results if not r.result]
        self.assertEqual(expected, output)

    def test_evaluate_sink_true(self):
        # Output sink returning true
        results = ShExEvaluator().evaluate(rdf, shex,  focus=list(self.g.subjects(RDF.type)),
                                           output_sink=self.create_sink())
        output = [(r.focus, r.reason) for r in results if not r.result]
        self.assertEqual(expected, self.messages)
        self.assertEqual([], output)

    def test_evaluate_sink_false(self):
        # Output sink returning false on first message
        ShExEvaluator().evaluate(self.g, shex, focus=list(self.g.subjects(RDF.type)),
                                 output_sink=self.create_sink(True))
        self.assertEqual(1, len(self.messages))
        self.assertEqual(list(expected)[0][1], self.messages[0][1])

    def test_evaluator_sink_(self):
        # Evaluator path

        results = ShExEvaluator(output_sink=self.create_sink()).evaluate(self.g, shex,
                                                                         focus=list(self.g.subjects(RDF.type)))
        output = [(r.focus, r.reason) for r in results if not r.result]
        self.assertEqual(expected, self.messages)
        self.assertEqual([], output)

    def test_cli_stoponerror(self):
        messages = StringIO()
        with redirect_stdout(messages):
            self.assertEqual(1, evaluate_cli([rdf, shex, '-A', '-ut']))
            self.assertEqual("""Errors:
  Focus: http://example.org/test/zrror1
  Start: http://example.org/test/S
  Reason:   Testing ex:zrror1 against shape http://example.org/test/S
       No matching triples found for predicate ex:foo

  Focus: http://example.org/test/zrror2
  Start: http://example.org/test/S
  Reason:   Testing ex:zrror2 against shape http://example.org/test/S
       No matching triples found for predicate ex:foo

  Focus: http://example.org/test/zrror3
  Start: http://example.org/test/S
  Reason:   Testing ex:zrror3 against shape http://example.org/test/S
       No matching triples found for predicate ex:foo

  Focus: http://example.org/test/zrror4
  Start: http://example.org/test/S
  Reason:   Testing ex:zrror4 against shape http://example.org/test/S
       No matching triples found for predicate ex:foo""", messages.getvalue().strip())

    def test_cli_stopafter(self):
        """
        Test the CLI stopafter parameter
        :return:
        """
        # 3 pass elements come first
        messages = StringIO()
        with redirect_stdout(messages):
            self.assertEqual(0, evaluate_cli([rdf, shex, '-A', '-ut', '--stopafter', '2']))
        self.assertEqual('', messages.getvalue())

        messages = StringIO()
        with redirect_stdout(messages):
            self.assertEqual(0, evaluate_cli([rdf, shex, '-A', '-ut', '--stopafter', '3']))
        messages = StringIO()
        with redirect_stdout(messages):
            self.assertEqual(1, evaluate_cli([rdf, shex, '-A', '-ut', '--stopafter', '4']))
        self.assertEqual("""Errors:
  Focus: http://example.org/test/zrror1
  Start: http://example.org/test/S
  Reason:   Testing ex:zrror1 against shape http://example.org/test/S
       No matching triples found for predicate ex:foo""", messages.getvalue().strip())
        

if __name__ == '__main__':
    unittest.main()
